#!/usr/bin/env python

import sys
from tools.session_calcer import SessionFeatureCalcer
from tools.session_reader import SessionReader

def main():
    for session in SessionReader().open(sys.argv[1]):
        result = []
        result += SessionFeatureCalcer(session).calc_features()
        print "\t".join(map(str, result))

if __name__ == "__main__":
    main()
