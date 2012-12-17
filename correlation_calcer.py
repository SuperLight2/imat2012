import sys
import os
import math

def calc_correlation(filepath):
    X = []
    Y = []
    for line in open(filepath):
        s = line.strip().split('\t')
        X.append(s[0])
        Y.append(s[1])
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
        descriptions.append(line.strip())
    for i in xrange(len(descriptions)):
        for j in xrange(len(descriptions)):
            if (i < j) and (descriptions[i].startswith('answer!')):
                os.system('cut -f %d,%d %s > tmp_correlation_file' % (i, j, pool_file))
                print "\t".join(map(str, [i, j, calc_correlation('tmp_correlation_file')]))
    os.system('rm -f tmp_correlation_file')



if __name__ == '__main__':
    main()
