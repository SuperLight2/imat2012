#!/usr/bin/env python

import sys
import sklearn
import scipy as sp
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cross_validation import ShuffleSplit

from auc_calcer import calc_auc

def Error(prediction, answer):
    error = 0
    for i in xrange(len(prediction)):
        result = 0
        if prediction[i][1] > prediction[i][0]:
            result = 1
        error += abs(result - answer[i])
    return 1.0 * error / len(prediction)

def calc_auc_on_prediction(prediction, answer):
    sub_result = []
    for i in xrange(len(prediction)):
        sub_result.append((prediction[i][1], answer[i]))
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
    # learn, sub_learn, validate, test
    # files in format: id switch [features]

    train_file = sys.argv[1]
    test_file = sys.argv[2]
    train_result_file = sys.argv[3]
    test_result_file = sys.argv[4]

    _X_learn = []
    _Y_learn = []
    _X_test = []

    print "Reading..."
    for line in open(train_file):
        rows = line.strip().split('\t')
        _Y_learn.append(int(rows[1]))
        _X_learn.append(rows[2:])

    for line in open(test_file):
        rows = line.strip().split('\t')
        _X_test.append(rows[2:])

    X_learn = np.array(_X_learn)
    Y_learn = np.array(_Y_learn)
    X_test = np.array(_X_test)

    print "Fitting..."
    bagging_iterations = 10
    error = 0
    rs = ShuffleSplit(len(Y_learn), n_iterations=bagging_iterations, test_size=0.8, random_state=1)
    result_on_test = {}
    result_on_learn = {}

    iteration = 0
    for train_index, test_index in rs:
        iteration += 1
        X_sub_learn, X_validate, Y_sub_learn, Y_validate = [0] * 4
        X_sub_learn, X_validate, Y_sub_learn, Y_validate = X_learn[train_index], X_learn[test_index], Y_learn[train_index], Y_learn[test_index]

        print "Training"
        #model = RandomForestClassifier(n_estimators = 15, max_depth = 7, verbose = 0, n_jobs = 5)
        model = GradientBoostingClassifier(n_estimators = 200, learn_rate=0.1, subsample = 0.8, max_depth = 6)
        model.fit(X_sub_learn, Y_sub_learn)

        print "Predicting"
        Y_prediction_on_validate = model.predict_proba(X_validate)
        current_error = Error(Y_prediction_on_validate, Y_validate)
        error += current_error
        print "Current error:\t", current_error
        print "Current AUC:\t", calc_auc_on_prediction(Y_prediction_on_validate, Y_validate)

        print "Learn predicting"
        add_to_result(model, X_learn, result_on_learn)
        print "Test predicting"
        add_to_result(model, X_test, result_on_test)

    error /= bagging_iterations
    print "Error on cross-validation:\t", error

    f_out = open(train_result_file, "w")
    for index in result_on_learn:
        print >> f_out, result_on_learn[index][1] / bagging_iterations
    f_out.close()

    f_out = open(test_result_file, "w")
    for index in result_on_test:
        print >> f_out, result_on_test[index][1] / bagging_iterations
    f_out.close()

if __name__ == '__main__':
    main()
