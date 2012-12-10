#!/usr/bin/env python

from optparse import OptionParser
import sys
from tools.ml_tools import calc_auc

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] [SESSION_ORDER_FILE [ANSWERS...]]
            Read classifier results from stdin and calc AUC.
            Results should be sorted in descending order of +1-class classification probability.
            If two args are given, then calculate AUC as in contest format.
            SESSION_ORDER_FILE - 1 column file with session_id`s in prediction order.
            ANSWER - 2 column file (answer, has_switch) with right asnwer.
            if session_id not in ASNWER file, it just will be ignored (so it can be usefull for validate sets)
    """)
    opts, args = optparser.parse_args()


    if len(args) == 2:
        answers = []
        for line in sys.stdin:
            if not line.strip():
                continue
            answers.append(int(line.strip()))
            print calc_auc(answers)
    else:
        for answer_filepath in args[1:]:
            answers = []
            right_answer = {}
            for line in open(answer_filepath):
                s = line.strip().split('\t', 4)
                session, has_switch = s[0], s[1]
                right_answer[session] = int(has_switch)
            for line in open(args[0]):
                session_id = int(line.strip())
                if session_id in right_answer:
                    answers.append(right_answer[session_id])
            print "AUC on %s:\t" % answer_filepath, calc_auc(answers)

if __name__ == '__main__':
    main()
