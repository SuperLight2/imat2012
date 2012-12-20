#!/usr/bin/env python

from optparse import OptionParser
from tools.session_reader import SessionReader

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] DATA_FILE""")
    opts, args = optparser.parse_args()

    data_file = args[0]
    queries_count = {}
    uniq_switch_count = {}
    switch_count = {}
    for session in SessionReader().open(data_file):
        for query in session.queries:
            if query.query_id not in queries_count:
                queries_count[query.query_id] = 0
                uniq_switch_count[query.query_id] = 0
                switch_count[query.query_id] = 0
            queries_count[query.query_id] += 1
            uniq_switch_count[query.query_id] += int(session.has_switch())
            switch_count[query.query_id] += len(session.switches)

    for query_id in queries_count.keys():
        print "\t".join(map(str,
            [query_id, queries_count[query_id], uniq_switch_count[query_id], switch_count[query_id]]))

if __name__ == "__main__":
    main()
