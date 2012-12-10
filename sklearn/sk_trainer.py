#!/usr/bin/env python

from optparse import OptionParser
import sklearn
import scipy as sp
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cross_validation import ShuffleSplit

from auc_calcer import calc_auc

def calc_auc_on_prediction(probability_prediction, answer):
    sub_result = []
    for i in xrange(len(probability_prediction)):
        sub_result.append((probability_prediction[i], answer[i]))
    return calc_auc([y[1] for y in sorted(sub_result, key=lambda x: -x[0])])

def add_to_result(model, X, result):
    Y = model.predict_proba(X)
    index = 0
    for prediction in Y:
        index += 1
        if index not in result:
            result[index] = None
        if result[index] is None:
            result[index] = prediction
        else:
            for j in xrange(len(result[index])):
                result[index][j] += prediction[j]

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE TRAIN_PREDICTION TEST_PREDICTION""")
    optparser.add_option('-b', '--bagging', dest='bagging_iterations',
        type='int', default=None,
        help='use bagging with iterations count.')
    optparser.add_option('-f', '--fraction', dest='fraction',
        type='float', default=1.0,
        help='sift learn pool with fraction probability')
    optparser.add_option('-i', '--iterations', dest='iterations',
        type='int', default=20,
        help='build iterations trees in one forest')
    opts, args = optparser.parse_args()

    train_file = args[0]
    test_file = args[1]
    train_result_file = args[2]
    test_result_file = args[3]

    _X_learn = []
    _Y_learn = []
    _X_test = []

    print "Reading Learn..."
    for line in open(train_file):
        rows = line.strip().split('\t')
        _Y_learn.append(int(rows[1]))
        _X_learn.append(rows[2:])

    print "Reading Test..."
    for line in open(test_file):
        rows = line.strip().split('\t')
        _X_test.append(rows[2:])

    X_learn = np.array(_X_learn)
    Y_learn = np.array(_Y_learn)
    X_test = np.array(_X_test)

    #model = RandomForestClassifier(n_estimators = 15, max_depth = 7, verbose = 0, n_jobs = 5)
    model = GradientBoostingClassifier(n_estimators = opts.iterations, learn_rate=0.1, subsample = 0.8, max_depth = 6)

    result_on_test = {}
    result_on_learn = {}

    if opts.bagging_iterations is None:
        opts.bagging_iterations = 1

        print "Training"
        model.fit(X_learn, Y_learn)

        print "Learn predicting"
        add_to_result(model, X_learn, result_on_learn)
        print "Test predicting"
        add_to_result(model, X_test, result_on_test)

        print "AUC on learn:\t", calc_auc_on_prediction(result_on_learn, Y_learn)
    else:
        error = 0
        rs = ShuffleSplit(len(Y_learn), n_iterations=opts.bagging_iterations, test_size=0.8, random_state=1)

        iteration = 0
        for train_index, test_index in rs:
            iteration += 1
            X_sub_learn, X_validate, Y_sub_learn, Y_validate = [0] * 4
            X_sub_learn, X_validate, Y_sub_learn, Y_validate = X_learn[train_index], X_learn[test_index], Y_learn[train_index], Y_learn[test_index]

            print "Training"
            model.fit(X_sub_learn, Y_sub_learn)

            print "Validate predicting"
            add_to_result(model, X_validate, result_on_learn)
            print "Test predicting"
            add_to_result(model, X_test, result_on_test)

            current_error = calc_auc_on_prediction(result_on_learn, Y_validate)
            error += current_error
            print "Current AUC on validate:\t", current_error

        error /= opts.bagging_iterations
        print "Error on cross-validation:\t", error

    f_out = open(train_result_file, "w")
    for prediction in result_on_learn:
        print >> f_out, prediction[1] / opts.bagging_iterations
    f_out.close()

    f_out = open(test_result_file, "w")
    for prediction in result_on_test:
        print >> f_out, prediction[1] / opts.bagging_iterations
    f_out.close()


if __name__ == '__main__':
    main()
