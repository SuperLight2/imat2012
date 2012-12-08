from features_calcer import FeaturesCalcer

class UserFeatureCalcer(FeaturesCalcer):
    def __init__(self, users_info):
        super(type(self), self).__init__()
        self.users_info = users_info

    def feature_user_info(self, session):
        """
        user_id of session
        user`s percentage of sessions with switch
        user`s percentage of sessions without clicks
        user`s clicks count
        user`s average clicks count on query
        """
        return self.users_info[session.user_id]
