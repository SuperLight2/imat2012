#!/usr/bin/env python

import sys

def main():
    for line in sys.stdin:
        s = line.strip().split('\t')
        print "\t".join(map(str, [s[0], s[1], "1", "1"] + s[2:]))

if __name__ == '__main__':
    main()
