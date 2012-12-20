#!/usr/bin/env python

from optparse import OptionParser

from tools.session_reader import SessionReader
from tools.queries_calcer import QueriesFeatureCalcer

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE STATISTIC_FILE""")
    optparser.add_option('-d', '--description', dest='description_file',
        metavar='FILE', type='string', default=None,
        help='filepath for features description')
    opts, args = optparser.parse_args()

    queries = {}
    for line in open(args[1]):
        s = line.strip().split('\t')
        query_id = int(s[0])
        queries[query_id] = map(float, s[1:])

    queries_features_calcer = QueriesFeatureCalcer(queries)
    for session in SessionReader().open(args[0]):
        print "\t".join(map(str, queries_features_calcer.calc_features(session)))
    if opts.description_file is not None:
        output_file = open(opts.description_file, 'w')
        print >> output_file, "\n".join(map(str, queries_features_calcer.get_description()))
        output_file.close()

if __name__ == '__main__':
    main()
