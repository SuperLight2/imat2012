import sys
import os
import math

def calc_correlation(filepath):
    X = []
    Y = []
    for line in open(filepath):
        s = line.strip().split('\t')
        X.append(float(s[0]))
        Y.append(float(s[1]))
    X_ = 1.0 * sum(X) / len(X)
    Y_ = 1.0 * sum(Y) / len(Y)
    X_2 = sum((x - X_) ** 2 for x in X)
    Y_2 = sum((y - Y_) ** 2 for y in Y)
    C = sum ((X[i] - X_) * (Y[i] - Y_) for i in xrange(len(X)))
    return 1.0 * C / math.sqrt(X_2 * Y_2)

def main():
    description_file = sys.argv[1]
    pool_file = sys.argv[2]

    descriptions = []
    for line in open(description_file):
        descriptions.append(line.strip().split('\t')[0:1])

    sum_1 = [0] * len(descriptions)
    sum_2 = [0] * len(descriptions)
    lines_count = 0

    print >> sys.stderr, "Calcing mean and varriance"
    for line in open(pool_file):
        lines_count += 1
        s = map(float, line.strip().split('\t'))
        for i in xrange(len(s)):
            sum_1[i] += s[i]
            sum_2[i] += s[i] ** 2
    mean = [1.0 * x / len(descriptions) for x in sum_1]
    var = [1.0 * (sum_2[i] - sum_1[i] ** 2) for i in xrange(len(descriptions))]
    C = [[0] * len(descriptions)] * len(descriptions)

    print >> sys.stderr, "Calcing correlation"
    for line in open(pool_file):
        s = map(float, line.strip().split('\t'))
        for i in xrange(len(s)):
            for j in xrange(len(s)):
                C[i][j] += (s[i] - mean[i]) * (s[j] - mean[j])
    for i in xrange(len(s)):
        for j in xrange(len(s)):
            C[i][j] /= math.sqrt(var[i])
            C[i][j] /= math.sqrt(var[j])

    for i in xrange(len(descriptions)):
        for j in xrange(len(descriptions)):
            if (i < j) and (descriptions[i][1].startswith('answer!')) and (not descriptions[j][1].startswith('answer!')):
                print "\t".join(map(str, [descriptions[i][0], descriptions[j][0], C[i][j]]))

if __name__ == '__main__':
    main()
