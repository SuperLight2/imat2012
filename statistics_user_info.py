#!/usr/bin/env python

import sys
from tools.session import *
from tools.session_reader import SessionReader

class UserInfo(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.sessions = 0
        self.sessions_without_clicks = 0
        self.sessions_with_switch = 0
        self.queries_count = 0
        self.clicks_count = 0

    def add(self, session):
        self.sessions += 1
        if session.has_switch():
            self.sessions_with_switch += 1

        added_clicks = 0
        for query in session.queries:
            self.queries_count += 1
            added_clicks += len(query.clicks)

        if added_clicks:
            self.clicks_count += added_clicks
        else:
            self.sessions_without_clicks += 1

    def flush(self):
        print "\t".join(map(str, [self.user_id, self.sessions, 1.0 * self.sessions_with_switch / self.sessions, 1.0 * self.sessions_without_clicks / self.sessions, self.clicks_count, 1.0 * self.clicks_count / self.queries_count]))


def main():
    users_info = {}

    for session in SessionReader().open(sys.argv[1]):
        user_id = session.user_id
        if user_id not in users_info:
            users_info[user_id] = UserInfo(user_id)
        users_info[user_id].add(session)
    for user, user_info in users_info.iteritems():
        user_info.flush()


if __name__ == '__main__':
    main()
