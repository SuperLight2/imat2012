from session import *

class SessionReader(object):
    def open(self, filepath):
        session = None
        for line in open(filepath):
            s = line.strip().split("\t")
            if s[2] == "M":
                if session is not None:
                    yield session
                session = Session(line)
            else:
                session.add(line)
        if session is not None:
            yield session

