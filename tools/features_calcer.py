import types
from time import time

class FeatureDescriptor(object):
    def __init__(self, name, description, calcing_time, value):
        self.name = name
        self.description = description
        self.calcing_time = calcing_time
        self.min = value
        self.max = value
        self.count = 1
        self.sum = value
        self.sum_sqr = value * value

    def add(self, value):
        self.count += 1
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.sum += value
        self.sum_sqr += value ** 2

    def get_description(self):
        X = 1.0 * self.sum / self.count
        X_2 = 1.0 * self.sum_sqr / self.count
        return [self.name, self.description, self.calcing_time,
                self.min, self.max, self.sum,
                self.sum_sqr, self.count, X, X_2 - X ** 2]


class FeaturesCalcer(object):
    def __init__(self):
        self.statistics = {}
        self.has_description = False
        self.feature_names = []

    def add_to_statistics(self, key, description, calcing_time, value):
        if key not in self.statistics:
            self.feature_names.append(key)
            self.statistics[key] = FeatureDescriptor(key, description, calcing_time, value)
        else:
            self.statistics[key].add(value)

    def get_description(self):
        result = []
        for name in self.feature_names:
            result.append("\t".join(map(str, self.statistics[name].get_description())))
        return result

    def calc_features(self, *args, **kwargs):
        result = []
        for method in dir(self):
            if not isinstance(getattr(self, method), types.MethodType):
                continue
            if not method.startswith("feature_"):
                continue
            feature_name = method[len("feature_"):]

            calcing_time = -time()
            sub_result = getattr(self, method)(*args, **kwargs)
            calcing_time += time()
            if not isinstance(sub_result, types.ListType):
                sub_result = [sub_result]

            description = getattr(self, method).__doc__
            if description is None:
                description = ""
            description = [s.strip() for s in description.strip().split('\n')]
            description += [''] * (len(sub_result) - len(description))

            for i in xrange(len(sub_result)):
                sub_feature_name = feature_name + ("" if len(sub_result) == 1 else "_" + str(i))
                self.add_to_statistics(sub_feature_name, description[i], calcing_time, sub_result[i])
            result += sub_result
        self.has_description = True
        return result
