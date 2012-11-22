from session import *

class SessionFeatureCalcer(object):
    def __init__(self, session):
        self.session = session

    def calc_features(self):
        results = [self.feature_day(), self.feature_has_click(), self.feature_session_duration()]
        results += self.features_avg_clicked_serps()
        results += self.features_serps_without_clicks()
        results += self.features_avg_time_for_click()
        return results

    def feature_day(self):
        return self.session.day % 7

    def feature_has_click(self):
        """ 1 if session has one or more clicks
        """
        has_click = False
        for query in self.session.queries:
            if len(query.clicks):
                has_click = True
                break
        return int(has_click)

    def features_avg_clicked_serps(self):
        """ for each query calc rate of clicked urls
        output the average rate, maximum and minimum
        """
        click_rate = []
        for query in self.session.queries:
            cur_result = 0
            all_urls = set(query.urls)
            clicked_urls = set()
            for click in query.clicks:
                clicked_urls.add(click.url_id)
            click_rate += [1.0 * len(clicked_urls) / len(all_urls)]
        return [sum(click_rate) / len(click_rate), max(click_rate), min(click_rate)]

    def features_serps_without_clicks(self):
        """ rate of serps with clicks
        """
        has_query_without_clicks = False
        serps_with_clicks = 0
        for query in self.session.queries:
            if len(query.clicks) == 0:
                has_query_without_clicks = True
            else:
                serps_with_clicks += 1
        return [int(has_query_without_clicks), 1.0 * serps_with_clicks / len(self.session.queries)]

    def features_avg_time_for_click(self):
        """ simple statistics of click times
        """
        first_click_time = []
        last_click_time = []
        for query in self.session.queries:
            query_time = query.time_passed
            click_times = []
            for click in query.clicks:
                click_times.append(click.time_passed - query_time)
            if len(click_times):
                first_click_time.append(min(click_times))
                last_click_time.append(max(click_times))
        if len(first_click_time):
            result = [min(first_click_time), max(first_click_time), 1.0 * sum(first_click_time) / len(first_click_time), max(last_click_time)]
        else:
            result = [-1] * 4
        return result

    def feature_session_duration(self):
        """ session duration time
        """
        max_time = 0
        for query in self.session.queries:
            max_time = max(max_time, query.time_passed)
            for click in query.clicks:
                max_time = max(max_time, click.time_passed)
        return max_time

