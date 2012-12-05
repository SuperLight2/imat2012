#!/usr/bin/env python

from optparse import OptionParser

from tools.session_reader import SessionReader
from tools.url_calcer import UrlFeatureCalcer

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE""")
    optparser.add_option('-d', '--description', dest='description_file',
        metavar='FILE', type='string', default=None,
        help='filepath for features description')
    opts, args = optparser.parse_args()

    urls = {}
    for line in open(args[1]):
        s = line.strip().split('\t')
        url = int(s[0])
        ctr = float(s[1])
        shows = int(s[2])
        urls[url] = (ctr, shows)

    url_features_calcer = UrlFeatureCalcer(urls)
    for session in SessionReader().open(args[0]):
        print "\t".join(map(str, url_features_calcer.calc_features(session)[1]))
    if opts.description_file is not None:
        output_file = open(opts.description_file, 'w')
        print >> output_file, "\n".join(map(str, url_features_calcer.calc_features(session)[1]))
        output_file.close()

if __name__ == '__main__':
    main()
