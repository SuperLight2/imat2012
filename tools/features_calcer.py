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
            result.append("\t".join(map(str,
                [name, self.statistics[name]['min'], self.statistics[name]['max'],
                 1.0 * self.statistics[name]['sum'] / self.statistics[name]['count'],
                 1.0 * self.statistics[name]['sum_sqr'] / self.statistics[name]['count'] - (1.0 * self.statistics[name]['sum'] / self.statistics[name]['count']) ** 2])))
        return result


    def calc_features(self, *args, **kwargs):
        result = []
        for method in dir(self):
            if method.startswith("feature_"):
                feature_name = method[len("feature_"):]
                if not self.has_description:
                    self.feature_names.append(feature_name)
                value = getattr(self, method)(*args, **kwargs)
                result += [value]
                self.add_to_statistics(feature_name, value)
            if method.startswith("features_"):
                sub_result = getattr(self, method)(*args, **kwargs)
                for i in xrange(len(sub_result)):
                    feature_name = method[len("feature_"):] + "_" + str(i)
                    if not self.has_description:
                        self.feature_names.append(feature_name)
                    self.add_to_statistics(feature_name, sub_result[i])
                result += sub_result
        self.has_description = True
        return result
