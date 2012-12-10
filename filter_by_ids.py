#!/usr/bin/env python

from optparse import OptionParser
import sys

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] IDS_FILE.
            Filter input stream by session_id ids""")
    optparser.add_option('-i', '--inverse', dest='inverse',
        default=False, action='store_true',
        help='inverse logic')
    opts, args = optparser.parse_args()

    ids = set()
    for line in open(args[0]):
        ids.add(line.strip())

    for line in sys.stdin:
        session_id = line.strip().split('\t', 2)[0]
        if (not opts.inverse) and (session_id in ids):
            continue
        if opts.inverse and (session_id not in ids):
            continue
        print line.strip()

if __name__ == '__main__':
    main()
