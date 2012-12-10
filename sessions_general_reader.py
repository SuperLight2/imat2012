#!/usr/bin/env python

from optparse import OptionParser

from tools.session_reader import SessionReader

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE""")
    opts, args = optparser.parse_args()

    for session in SessionReader().open(args[0]):
        print session.user_id

if __name__ == "__main__":
    main()
