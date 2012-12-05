from features_calcer import FeaturesCalcer

class SessionIdAndSwitchFeatureCalcer(FeaturesCalcer):
    def feature_id(self, session):
        return session.session_id

    def feature_switch(self, session):
        return 1 if session.has_switch() else 0

