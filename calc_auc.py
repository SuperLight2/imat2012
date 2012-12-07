#!/usr/bin/env python

import sys
from tools.ml_tools import calc_auc

def main():
    if (len(sys.argv) > 1) and (sys.argv[1] == '-h'):
        print >> sys.stderr, "Read classifier results. Results should be sorted in descending order of +1-class classification probability"
        return

    answers = []
    for line in sys.stdin:
        if not line.strip():
            continue
        answers.append(int(line.strip()))
    print calc_auc(answers)

if __name__ == '__main__':
    main()
