from features_calcer import FeaturesCalcer

class QueriesFeatureCalcer(FeaturesCalcer):
    def __init__(self, queries):
        super(type(self), self).__init__()
        self.queries = queries

    def feature_queries_in_session(self, session):
        """
        max query popularity in session
        min query popularity in session
        average query popularity in session
        max query uniq switch count in session
        min query uniq switch count in session
        average query uniq switch count in session
        max query switch count in session
        min query switch count in session
        average query switch count in session
        """
        populatities = []
        switch_count = []
        uniq_switch_count = []
        for query in session.queries:
            if query.query_id in self.queries:
                populatities.append(self.queries[query.query_id][0])
                switch_count.append(self.queries[query.query_id][1])
                uniq_switch_count.append(self.queries[query.query_id][2])
            else:
                populatities.append(0)
                switch_count.append(0)
                uniq_switch_count.append(0)
        return [max(populatities), min(populatities), 1.0 * sum(populatities) / len(populatities),
                max(switch_count), min(switch_count), 1.0 * sum(switch_count) / len(switch_count),
                max(uniq_switch_count), min(uniq_switch_count), 1.0 * sum(uniq_switch_count) / len(uniq_switch_count)]