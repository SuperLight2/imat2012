from features_calcer import FeaturesCalcer

class SessionIdAndSwitchFeatureCalcer(FeaturesCalcer):
    def feature_id(self, session):
        """
        session_id
        """
        return session.session_id

    def feature_switch(self, session):
        """
        answer! session has switch
        answer! classes for multiclassification
        answer! ratings for regression
        """
        result = [1 if session.has_switch() else 0]
        if len(session.switches) == 0:
            result += [0]
        elif len(session.switches) == 1:
            result += [1]
        elif len(session.switches) < 4:
            result += [2]
        else:
            result += [3]
        result += [1.0 * (0.5 + len(session.switches)) / (0.5 + len(session.queries))]
        return result

