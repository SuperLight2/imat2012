#!/usr/bin/env python

from optparse import OptionParser
import sys
from tools.ml_tools import calc_auc

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] [SESSION_ORDER_FILE ANSWER]
            Read classifier results from stdin and calc AUC.
            Results should be sorted in descending order of +1-class classification probability.
            If two args are given, then calculate AUC as in contest format.
            SESSION_ORDER_FILE - 1 column file with session_id`s in prediction order.
            ANSWER - 2 column file (answer, has_switch) with right asnwer.
    """)
    opts, args = optparser.parse_args()

    answers = []
    if len(args) == 2:
        for line in sys.stdin:
            if not line.strip():
                continue
            answers.append(int(line.strip()))
    else:
        right_answer = {}
        for line in open(args[1]):
            session, has_switch = line.strip().split('\t')
            right_answer[session] = int(has_switch)
        for line in open(args[0]):
            if not line.strip():
                continue
            answers.append(right_answer[line.strip()])
        if len(right_answer) != len(answers):
            raise "The length of given files should be equal"
    print calc_auc(answers)

if __name__ == '__main__':
    main()
