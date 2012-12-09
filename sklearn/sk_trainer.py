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

def main():
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    train_result_file = sys.argv[3]
    test_result_file = sys.argv[4]

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

    print "Training"
    #model = RandomForestClassifier(n_estimators = 15, max_depth = 7, verbose = 0, n_jobs = 5)
    model = GradientBoostingClassifier(n_estimators = 100, learn_rate=0.1, subsample = 0.8, max_depth = 6)
    model.fit(X_learn, Y_learn)

    print "Learn Predicting"
    Y_prediction_on_learn = model.predict_proba(X_learn)
    print "Error on learn:\t", Error(Y_prediction_on_learn, Y_learn)
    print "Current AUC:\t", calc_auc_on_prediction(Y_prediction_on_learn, Y_learn)
    f_out = open(train_result_file, "w")
    for prediction in Y_prediction_on_learn:
        print >> f_out, prediction[1]
    f_out.close()

    print "Test predicting"
    Y_test = model.predict_proba(X_test)
    f_out = open(test_result_file, "w")
    for prediction in Y_test:
        print >> f_out, prediction[1]
    f_out.close()


if __name__ == '__main__':
    main()
