#!/usr/bin/env python

from optparse import OptionParser
from tools.session_reader import SessionReader

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] DATA_FILE""")
    opts, args = optparser.parse_args()

    data_file = args[0]
    queries_count = {}
    for session in SessionReader().open(data_file):
        for query in session.queries:
            if query.query_id not in queries_count:
                queries_count[query.query_id] = 0
            queries_count[query.query_id] += 1

    for key, value in queries_count.iteritems():
        print key, "\t", value

if __name__ == "__main__":
    main()
