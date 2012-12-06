from features_calcer import FeaturesCalcer

class UrlFeatureCalcer(FeaturesCalcer):
    def __init__(self, urls):
        super(type(self), self).__init__()
        self.urls = urls

    def feature_urls_in_session(self, session):
        urls_showed = set()
        for query in session.queries:
            for url in query.urls:
                if url in self.urls:
                    urls_showed.add(url)
        return len(urls_showed)

    def feature_crt_for_urls(self, session):
        shows = {}
        clicks = {}
        for url in self.urls:
            shows[url] = 0
            clicks[url] = 0

        for query in session.queries:
            for url in query.urls:
                if url in self.urls:
                    shows[url] += 1
                    for click in query.clicks:
                        if click.url_id == url:
                            clicks[url] += 1
                            break
        ctrs = []
        for url in self.urls:
            if shows[url] > 0:
                ctrs.append(1.0 * clicks[url] / shows[url])
        return [1.0 * sum(ctrs) / len(ctrs)] if len(ctrs) else [0]

    def feature_click_time_for_urls(self, session):
        time = {}
        for url in self.urls:
            time[url] = -1

        for query in session.queries:
            for url in query.urls:
                if url in self.urls:
                    for click in query.clicks:
                        if click.url_id == url:
                            if (time[url] == -1) or (time[url] > click.time_passed):
                                time[url] = click.time_passed
        times = []
        for url in self.urls:
            if time[url] != -1:
                times.append(time[url])
        return [min(times), max(times), 1.0 * sum(times) / len(times)] if len(times) else [1000000] * 3

