#!/usr/bin/env python

from optparse import OptionParser
from tools.session_reader import SessionReader

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] DATA_FILE TOP_SIZE RESULT_SIZE COEFFICIENT""")
    opts, args = optparser.parse_args()

    data_file = args[0]
    top_size = int(args[1])
    result_size = int(args[2])
    coefficient = None
    if len(args) == 4:
        coefficient = float(args[3])

    url_in_top = {}
    url_clicks = {}
    for session in SessionReader().open(data_file):
        for query in session.queries:
            for url in query.urls[:top_size]:
                if url not in url_in_top:
                    url_in_top[url] = 0
                    url_clicks[url] = 0
                url_in_top[url] += 1
                for click in query.clicks:
                    if click.url_id == url:
                        url_clicks[url] += 1
                        break

    urls = []
    for url in url_clicks:
        urls.append((url, 1.0 * url_clicks[url] / url_in_top[url], url_in_top[url]))
    urls.sort(key=lambda x: (x[1], x[2]))
    if coefficient is not None:
        urls.sort(key=lambda x: (coefficient * x[1]  + (1 - coefficient) * x[2]))
    for url_info in urls[-result_size:]:
        print "\t".join(map(str, url_info))

if __name__ == "__main__":
    main()
