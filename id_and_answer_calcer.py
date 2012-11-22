#!/usr/bin/env python

import sys
from tools.session import *
from tools.session_reader import SessionReader

def main():
    for session in SessionReader().open(sys.argv[1]):
        result = [session.session_id, 1 if session.has_switch() else 0]
        print "\t".join(map(str, result))

if __name__ == "__main__":
    main()
