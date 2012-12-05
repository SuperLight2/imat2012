from features_calcer import FeaturesCalcer

class SessionFeatureCalcer(FeaturesCalcer):
    def features_days(self, session):
        result = []
        for i in xrange(6):
            result.append(session.day % (i + 2))
        return result

    def feature_has_click(self, session):
        """ 1 if session has one or more clicks
        """
        has_click = False
        for query in session.queries:
            if len(query.clicks):
                has_click = True
                break
        return int(has_click)

    def features_avg_clicked_serps(self, session):
        """ for each query calc rate of clicked urls
        output the average rate, maximum and minimum
        """
        click_rate = []
        for query in session.queries:
            cur_result = 0
            all_urls = set(query.urls)
            clicked_urls = set()
            for click in query.clicks:
                clicked_urls.add(click.url_id)
            click_rate += [1.0 * len(clicked_urls) / len(all_urls)]
        return [sum(click_rate) / len(click_rate), max(click_rate), min(click_rate)]

    def features_serps_without_clicks(self, session):
        """ rate of serps with clicks
        """
        has_query_without_clicks = False
        serps_with_clicks = 0
        for query in session.queries:
            if len(query.clicks) == 0:
                has_query_without_clicks = True
            else:
                serps_with_clicks += 1
        return [int(has_query_without_clicks), 1.0 * serps_with_clicks / len(session.queries)]

    def features_avg_time_for_click(self, session):
        """ simple statistics of click times
        """
        first_click_time = []
        last_click_time = []
        for query in session.queries:
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

    def feature_click_count(self, session):
        """ session's click count
        """
        click_count = 0
        for query in session.queries:
            click_count += len(query.clicks)
        return click_count

    def feature_queries_count(self, session):
        """ session's queries count
        """
        return len(session.queries)

    def features_avg_time_between_event(self, session):
        """ statistics of click times
        """
        click_times = []
        click_times_in_query = []
        for query in session.queries:
            query_time = query.time_passed
            times_in_query = []
            for click in query.clicks:
                times_in_query.append(click.time_passed - query_time)
                click_times.append(click.time_passed - query_time)
            
            if len(times_in_query):
                click_times_in_query.append(1.0 * sum(times_in_query) / len(times_in_query))
        if len(click_times):
            result = [1.0 * sum(click_times) / len(click_times), 1.0 * sum(click_times_in_query) / len(click_times_in_query)]
        else:
            result = [-1] * 2
        return result

    def features_avg_time_between_click_to_click(self, session):
        """ statistics of click times
        """
        click_times = []
        click_times_in_query = []
        for query in session.queries:
            old_time = query.time_passed
            times_in_query = []
            for click in query.clicks:
                times_in_query.append(click.time_passed - old_time)
                click_times.append(click.time_passed - old_time)
                old_time = click.time_passed
            
            if len(times_in_query):
                click_times_in_query.append(1.0 * sum(times_in_query) / len(times_in_query))
        if len(click_times):
            result = [1.0 * sum(click_times) / len(click_times), 1.0 * sum(click_times_in_query) / len(click_times_in_query)]
        else:
            result = [-1] * 2
        return result

    def features_avg_time_between_click_to_query(self, session):
        """ statistics of click times
        """
        sum_1 = 0
        sum_2 = 0
        old_time = 0
        for query in session.queries:
            sum_1 += query.time_passed - old_time
            sum_2 += (query.time_passed - old_time) * (query.time_passed - old_time)
            for click in query.clicks:
                old_time = click.time_passed

        return [sum_1, sum_2]

    def features_click_on_urls(self, session):
        """ click_on_urls
        """
        click_on_urls_with_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for query in session.queries:
            for click in query.clicks:
                click_on_urls_with_number[query.urls.index(click.url_id)] += 1
        return click_on_urls_with_number

    def feature_avg_click_on_urls(self, session):
        """ avg_click_on_urls
        """
        click_avg_on_urls = []
        for query in session.queries:
            for click in query.clicks:
                click_avg_on_urls.append(query.urls.index(click.url_id))
        if len(click_avg_on_urls):
            result = 1.0 * sum(click_avg_on_urls) / len(click_avg_on_urls)
        else:
            result = 11
        return result

    def feature_first_query_id(self, session):
        """ session user id
        """
        if len(session.queries):
            return session.queries[0].query_id
        else:
            return 0

    def feature_session_duration(self, session):
        """ session duration time
        """
        max_time = 0
        for query in session.queries:
            max_time = max(max_time, query.time_passed)
            for click in query.clicks:
                max_time = max(max_time, click.time_passed)
        return max_time

