#!/usr/bin/env python

class Click(object):
    def __init__(self, line):
        s = line.strip().split('\t')
        self.time_passed = int(s[1])
        self.serp_id = int(s[3])
        self.url_id = int(s[4])

class Query(object):
    def __init__(self, line):
        s = line.strip().split('\t')
        self.time_passed = int(s[1])
        self.serp_id = int(s[3])
        self.query_id = int(s[4])
        self.urls = map(int, s[5:])
        self.clicks = []

class Switch(object):
    def __init__(self, line):
        self.time_passed = int(line.strip().split('\t')[1])


class Session(object):
    def __init__(self, line):
        s = line.strip().split('\t')
        self.session_id = int(s[0])
        self.day = int(s[1])
        self.user_id = int(s[3])
        self.swith_type = None
        if len(s) == 5:
            self.swith_type = s[4]

        self.switches = []
        self.queries = []

    def add(self, line):
        s = line.strip().split('\t')
        type_of_record = s[2]

        if type_of_record == 'Q':
            query = Query(line)
            self.queries.append(query)

        if type_of_record == 'C':
            click = Click(line)
            for query in self.queries:
                if click.serp_id == query.serp_id:
                    query.clicks.append(click)

        if type_of_record == 'S':
            switch = Switch(line)
            self.switches.append(switch)

    def has_switch(self):
        return len(self.switches)

