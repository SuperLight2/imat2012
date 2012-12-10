#!/usr/bin/env python

import sys
from tools.session_reader import SessionReader

class UserInfo(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.sessions = 0
        self.sessions_without_clicks = 0
        self.sessions_with_switch = 0
        self.queries_count = 0
        self.clicks_count = 0
        self.switch_count = 0
        self.switch_time_sum = 0
        self.click_times_sum = 0
        self.click_time_query_sum = 0
        self.first_click_time_query_sum = 0

        self.ctr_length = 10
        self.ctr_clicks = [0] * self.ctr_length
        self.ctr_shows = [0] * self.ctr_length

    def add(self, session):
        self.sessions += 1
        if session.has_switch():
            self.sessions_with_switch += 1
        self.switch_count += len(session.switches)
        for switch in session.switches:
            self.switch_time_sum += switch.time_passed

        added_clicks = 0
        for query in session.queries:
            self.queries_count += 1
            added_clicks += len(query.clicks)

            clicked_position = [False] * min(self.ctr_length, len(query.urls))
            for click in query.clicks:
                clicked_position[query.urls.index(click.url_id)] = True
                self.click_times_sum + click.time_passed
                self.click_time_query_sum += (click.time_passed - query.time_passed)
            if len(query.clicks):
                self.first_click_time_query_sum += query.clicks[0].time_passed - query.time_passed

            for index in xrange(len(clicked_position)):
                if clicked_position[index]:
                    self.ctr_clicks[index] += 1
                self.ctr_shows[index] += 1

        if added_clicks:
            self.clicks_count += added_clicks
        else:
            self.sessions_without_clicks += 1

    def flush(self):
        ctrs = [0] * self.ctr_length
        for i in xrange(self.ctr_length):
            if self.ctr_shows[i]:
                ctrs[i] = 1.0 * self.ctr_clicks[i] / self.ctr_shows[i]
            else:
                ctrs[i] = 0

        print "\t".join(map(str, [self.user_id, self.sessions,
                                  1.0 * self.sessions_with_switch / self.sessions,
                                  1.0 * self.sessions_without_clicks / self.sessions,
                                  self.clicks_count,
                                  self.switch_count,
                                  1.0 * self.switch_count / self.queries_count,
                                  1.0 * self.clicks_count / self.queries_count,
                                  1.0 * self.switch_time_sum / self.switch_count,
                                  1.0 * self.click_times_sum / self.sessions,
                                  1.0 * self.click_time_query_sum / self.queries_count,
                                  1.0 * self.first_click_time_query_sum / self.queries_count,
                                  "\t".join(map(str, ctrs))]))


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
