from features_calcer import FeaturesCalcer

class SessionFeatureCalcer(FeaturesCalcer):
    def feature_days(self, session):
        """
        day module 7
        """
        return session.day % 7

    def feature_has_click(self, session):
        """
        session has click
        """
        has_click = False
        for query in session.queries:
            if len(query.clicks):
                has_click = True
                break
        return int(has_click)

    def feature_avg_clicked_serps(self, session):
        """
        average percentage of clicked urls in serp
        maximum percentage of clicked urls in serp
        minimum percentage of clicked urls in serp
        """
        click_rate = []
        for query in session.queries:
            all_urls = set(query.urls)
            clicked_urls = set()
            for click in query.clicks:
                clicked_urls.add(click.url_id)
            click_rate += [1.0 * len(clicked_urls) / len(all_urls)]
        return [sum(click_rate) / len(click_rate), max(click_rate), min(click_rate)]

    def feature_serps_without_clicks(self, session):
        """
        session has query without clicks
        percentage of serps in session with clicks
        """
        has_query_without_clicks = False
        serps_with_clicks = 0
        for query in session.queries:
            if len(query.clicks) == 0:
                has_query_without_clicks = True
            else:
                serps_with_clicks += 1
        return [int(has_query_without_clicks), 1.0 * serps_with_clicks / len(session.queries)]

    def feature_avg_time_for_click(self, session):
        """
        minimum time in all serp of first click (-1)
        maximum time in all serp of first click (-1)
        average time in all serp of first click (-1)
        maximum time in all serp of last click (-1)
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
        """
        clicks count in session
        """
        click_count = 0
        for query in session.queries:
            click_count += len(query.clicks)
        return click_count

    def feature_queries_count(self, session):
        """
        queries count in session
        queries count in session without clicks
        first query clicks count
        """
        queries_without_clicks = 0
        for query in session.queries:
            if not len(query.clicks):
                queries_without_clicks += 1
        return [len(session.queries), queries_without_clicks, len(session.queries[0].clicks)]

    def feature_avg_time_between_event(self, session):
        """
        average time of all click times in serps (-1)
        average time of average click times in serps (-1)
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

    def feature_avg_time_between_click_to_click(self, session):
        """
        average dweltime between all clicks (-1)
        average of average dweltimes between all clicks in serps (-1)
        maximum of average dweltimes between all clicks in serps (-1)
        percentage of long clicks (-1)
        percentage of super long clicks (-1)
        """
        long_click_duration = 3000
        super_long_click_duration = 9000
        long_clicks_count = 0
        super_long_clicks_count = 0
        click_times = []
        click_times_in_query = []
        for query in session.queries:
            old_time = query.time_passed
            times_in_query = []
            for click in query.clicks:
                duration = click.time_passed - old_time
                times_in_query.append(duration)
                click_times.append(duration)
                if duration >= long_click_duration:
                    long_clicks_count += 1
                if duration >= super_long_click_duration:
                    super_long_clicks_count += 1
                old_time = click.time_passed
            
            if len(times_in_query):
                click_times_in_query.append(1.0 * sum(times_in_query) / len(times_in_query))
        if len(click_times):
            result = [1.0 * sum(click_times) / len(click_times),
                      1.0 * sum(click_times_in_query) / len(click_times_in_query),
                      max(click_times),
                      1.0 * long_clicks_count / len(click_times),
                      1.0 * super_long_clicks_count / len(click_times)]
        else:
            result = [-1] * 5
        return result

    def feature_avg_time_between_click_to_query(self, session):
        """
        sum of times between query and last click
        sum of squares of times between query and last click
        mean of times between query and last click
        variance of times between query and last click
        """
        sum = 0
        sum_sqr = 0
        old_time = 0
        for query in session.queries:
            sum += query.time_passed - old_time
            sum_sqr += (query.time_passed - old_time) * (query.time_passed - old_time)
            for click in query.clicks:
                old_time = click.time_passed
        X = 1.0 * sum / len(session.queries)
        X_2 = 1.0 * sum_sqr / len(session.queries)
        return [sum, sum_sqr, X, X_2 - X ** 2]

    def feature_urls_shown(self, session):
        """
        maximum number of shown urls in serps
        minimum number of shown urls in serps
        average number of shown urls in serps
        """
        shown = []
        for query in session.queries:
            shown.append(len(query.urls))
        return [max(shown), min(shown), 1.0 * sum(shown) / len(shown)]

    def feature_click_on_urls(self, session):
        """
        clicks count on 1-position
        clicks count on 2-position
        clicks count on 3-position
        clicks count on 4-position
        clicks count on 5-position
        clicks count on 6-position
        clicks count on 7-position
        clicks count on 8-position
        clicks count on 9-position
        clicks count on 10-position
        """
        click_on_urls_with_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for query in session.queries:
            for click in query.clicks:
                click_on_urls_with_number[query.urls.index(click.url_id)] += 1
        return click_on_urls_with_number

    def feature_session_ctrs(self, session):
        """
        session_ctr_on_url_1 (0)
        session_ctr_on_url_2 (0)
        session_ctr_on_url_3 (0)
        session_ctr_on_url_4 (0)
        session_ctr_on_url_5 (0)
        session_ctr_on_url_6 (0)
        session_ctr_on_url_7 (0)
        session_ctr_on_url_8 (0)
        session_ctr_on_url_9 (0)
        session_ctr_on_url_10 (0)
        """
        ctrs_length = 10
        clicks = [0] * ctrs_length
        shows = [0] * ctrs_length
        for query in session.queries:
            has_click = [False] * min(ctrs_length, len(query.urls))
            for click in query.clicks:
                has_click[query.urls.index(click.url_id)] = True
            for index in xrange(len(has_click)):
                if has_click[index]:
                    clicks[index] += 1
                shows[index] += 1
        ctrs = [0] * ctrs_length
        for i in xrange(ctrs_length):
            if shows[i]:
                ctrs[i] = 1.0 * clicks[i] / shows[i]
            else:
                ctrs[i] = 0
        return ctrs

    def feature_inverse_count(self, session):
        """
        percentage of queries with inverse clicks
        percentage of queries with inverse clicks in top3
        """
        inverses = 0
        inverses_in_top3 = 0
        for query in session.queries:
            positions = []
            for click in query.clicks:
                positions.append(query.urls.index(click.url_id))
            has_inverse = False
            has_inverse_in_top3 = False
            for i in xrange(1, len(positions)):
                if positions[i] < positions[i - 1]:
                    has_inverse = True
                    if i < 3:
                        has_inverse_in_top3 = True
            inverses += int(has_inverse)
            inverses_in_top3 += int(has_inverse_in_top3)
        return [1.0 * inverses / len(session.queries), 1.0 * inverses_in_top3 / len(session.queries)]

    def feature_queries_wo_clicks_in_top(self, session):
        """
        percentage of queries without clicks in top1
        percentage of queries without clicks in top2
        percentage of queries without clicks in top3
        percentage of queries without clicks in top4
        percentage of queries without clicks in top5
        """
        result = [0] * 5
        for query in session.queries:
            has_click_in_top = [False] * len(result)
            for click in query.clicks:
                position = query.urls.index(click.url_id)
                for i in xrange(min(position + 1, len(result))):
                    has_click_in_top[i] = True
            for i in xrange(len(has_click_in_top)):
                if not has_click_in_top[i]:
                    result[i] += 1
        return [1.0 * x / len(session.queries) for x in result]


    def feature_avg_click_on_urls(self, session):
        """
        mean of clicks position (10)
        variance of clicks position (10000)
        """
        click_avg_on_urls = []
        for query in session.queries:
            for click in query.clicks:
                click_avg_on_urls.append(query.urls.index(click.url_id))
        if len(click_avg_on_urls):
            X = 1.0 * sum(click_avg_on_urls) / len(click_avg_on_urls)
            X_2 = 1.0 * sum([x ** 2 for x in click_avg_on_urls]) / len(click_avg_on_urls)
            return [X, X_2 - X ** 2]
        else:
            return [10, 10000]

    def feature_session_duration(self, session):
        """
        session duration time
        """
        max_time = 0
        for query in session.queries:
            max_time = max(max_time, query.time_passed)
            for click in query.clicks:
                max_time = max(max_time, click.time_passed)
        return max_time

