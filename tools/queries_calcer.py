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
        """
        populatities = []
        for query in session.queries:
            if query.query_id in self.queries:
                populatities.append(self.queries[query.query_id])
            else:
                populatities.append(0)
        return [max(populatities), min(populatities), 1.0 * sum(populatities) / len(populatities)]