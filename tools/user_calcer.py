from features_calcer import FeaturesCalcer

class UserFeatureCalcer(FeaturesCalcer):
    def __init__(self, users_info):
        super(type(self), self).__init__()
        self.users_info = users_info

    def feature_user_info(self, session):
        """
        user`s count of sessions
        user`s percentage of sessions with switch
        user`s percentage of sessions without clicks
        user`s clicks count
        user`s switch count
        user`s switch count / queries count
        user`s average clicks count on query
        user`s average switch time
        user`s average click time
        user`s average click time in query
        user`s average first click time in query
        user`s ctr1
        user`s ctr2
        user`s ctr3
        user`s ctr4
        user`s ctr5
        user`s ctr6
        user`s ctr7
        user`s ctr8
        user`s ctr9
        user`s ctr10
        """
        return self.users_info[session.user_id]
