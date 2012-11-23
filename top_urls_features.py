#!/usr/bin/env python

import sys
from tools.session_reader import SessionReader
from tools.url_calcer import UrlFeatureCalcer


def main():
    urls = {}

    for line in open(sys.argv[2]):
        s = line.strip().split('\t')
        url = s[0]
        ctr = float(s[1])
        shows = int(s[2])
        urls[url] = (ctr, shows)

    url_features_calcer = UrlFeatureCalcer(urls)
    for session in SessionReader().open(sys.argv[1]):
        result = []
        result += url_features_calcer.calc_features(session)
        print "\t".join(map(str, result))

if __name__ == '__main__':
    main()
