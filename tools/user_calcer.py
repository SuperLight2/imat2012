from features_calcer import FeaturesCalcer

class UserFeatureCalcer(FeaturesCalcer):
    def __init__(self, users_info):
        self.users_info = users_info

    def features_user_info(self, session):
        return self.users_info[session.user_id]
