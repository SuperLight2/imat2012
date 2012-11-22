#!/usr/bin/env python

import sys
from tools.session import *
from tools.session_reader import SessionReader

def main():
    users = {}

    for line in open(sys.argv[2]):
        s = line.strip().split('\t')
        user = s[0]
        info = s[1:]
        users[user] = info

    for session in SessionReader().open(sys.argv[1]):
        print "\t".join(map(str, users[session.user_id]))

if __name__ == '__main__':
    main()
