class FeaturesCalcer(object):
    def calc_features(self, *args, **kwargs):
        result = []
        description = []
        for method in dir(self):
            if method.startswith("feature_"):
                description.append(method[len("feature_"):])
                result += [getattr(self, method)(*args, **kwargs)]
            if method.startswith("features_"):
                sub_result = getattr(self, method)(*args, **kwargs)
                for i in xrange(len(sub_result)):
                    description.append(method[len("features_"):] + "_" + str(i))
                result += sub_result
        return result, description
