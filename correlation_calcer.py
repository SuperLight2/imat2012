import sys
import math

def main():
    description_file = sys.argv[1]
    pool_file = sys.argv[2]

    descriptions = []
    for line in open(description_file):
        s = line.strip().split('\t')
        descriptions.append([s[0], s[1]])

    sum_1 = [0] * len(descriptions)
    sum_2 = [0] * len(descriptions)
    prod = [0] * len(descriptions)
    C = [0] * len(descriptions)
    for i in xrange(len(descriptions)):
        prod[i] = [0] * len(descriptions)
        C[i] = [0] * len(descriptions)
    lines_count = 0

    for line in open(pool_file):
        lines_count += 1
        s = map(float, line.strip().split('\t'))
        for i in xrange(len(s)):
            sum_1[i] += s[i]
            sum_2[i] += s[i] * s[i]
            for j in xrange(len(descriptions)):
                if (i < j) and (descriptions[i][1].startswith('answer!')) and (not descriptions[j][1].startswith('answer!')):
                    prod[i][j] += s[i] * s[j]

    for i in xrange(len(descriptions)):
        for j in xrange(len(descriptions)):
            if (i < j) and (descriptions[i][1].startswith('answer!')) and (not descriptions[j][1].startswith('answer!')):
                C[i][j] = (lines_count * prod[i][j] - sum_1[i] * sum_1[j])
                if abs(lines_count * sum_2[i] - sum_1[i] * sum_1[i]) > 1e-8 and abs(lines_count * sum_2[j] - sum_1[j] * sum_1[j]) > 1e-8:
                    C[i][j] /= math.sqrt(lines_count * sum_2[i] - sum_1[i] * sum_1[i])
                    C[i][j] /= math.sqrt(lines_count * sum_2[j] - sum_1[j] * sum_1[j])
                else:
                    C[i][j] = 0
                print "\t".join(map(str, [descriptions[i][0], descriptions[j][0], C[i][j]]))

if __name__ == '__main__':
    main()