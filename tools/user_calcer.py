from features_calcer import FeaturesCalcer

class UserFeatureCalcer(FeaturesCalcer):
    def __init__(self, users_info):
        super(type(self), self).__init__()
        self.users_info = users_info

    def feature_user_info(self, session):
        return self.users_info[session.user_id]
