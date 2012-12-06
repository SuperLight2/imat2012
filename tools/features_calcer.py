import types

class FeaturesCalcer(object):
    def __init__(self):
        self.statistics = {}
        self.has_description = False
        self.feature_names = []

    def add_to_statistics(self, key, value):
        if key not in self.statistics:
            self.statistics[key] = {
                'count': 1,
                'min': value,
                'max': value,
                'sum': value,
                'sum_sqr': value * value
            }
        else:
            self.statistics[key]['count'] += 1
            self.statistics[key]['min'] = min(self.statistics[key]['min'], value)
            self.statistics[key]['max'] = max(self.statistics[key]['max'], value)
            self.statistics[key]['sum'] += value
            self.statistics[key]['sum_sqr'] += value * value

    def get_description(self):
        result = []
        for name in self.feature_names:
            X = 1.0 * self.statistics[name]['sum'] / self.statistics[name]['count']
            X_2 = 1.0 * self.statistics[name]['sum_sqr'] / self.statistics[name]['count']
            result.append("\t".join(map(str,
                [name, self.statistics[name]['min'], self.statistics[name]['max'], X, X_2 - X * X])))
        return result

    def calc_features(self, *args, **kwargs):
        result = []
        for method in dir(self):
            if not isinstance(getattr(self, method), types.MethodType):
                continue
            feature_name = method[len("feature_"):]
            sub_result = getattr(self, method)(*args, **kwargs)
            if not isinstance(sub_result, types.ListType):
                sub_result = [sub_result]
            for i in xrange(len(sub_result)):
                sub_feature_name = feature_name
                if len(sub_result) > 1:
                    sub_feature_name += "_" + str(i)
                if not self.has_description:
                    self.feature_names.append(sub_feature_name)
                self.add_to_statistics(sub_feature_name, sub_result[i])
            result += sub_result
        self.has_description = True
        return result
