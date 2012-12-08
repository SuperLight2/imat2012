from features_calcer import FeaturesCalcer

class SessionIdAndSwitchFeatureCalcer(FeaturesCalcer):
    def feature_id(self, session):
        """
        session_id
        """
        return session.session_id

    def feature_switch(self, session):
        """
        session has switch
        """
        return 1 if session.has_switch() else 0

