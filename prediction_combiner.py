from optparse import OptionParser

def try_to_float(s):
    try:
        value = float(s)
    except ValueError:
        return False, 0
    return True, value

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] [[WEIGHT ]PREDICTION_FILE] .. [[WEIGHT ]PREDICTION_FILE]""")
    optparser.add_option('-m', '--mapping', dest='use_mapping',
        default=False, action='store_true',
        help='use mapping to [0, 1] for each prediction file')
    opts, args = optparser.parse_args()

    files_to_combine = []
    weights = []

    current_weight = 1.0
    for filepath in args:
        is_float, value = try_to_float(filepath)
        if not is_float:
            files_to_combine.append(filepath)
            weights.append(current_weight)
            current_weight = 1.0
        else:
            current_weight = value

    result = {}
    for index in xrange(len(files_to_combine)):
        filepath = files_to_combine[index]
        maximum = 1
        minimum = 0
        if opts.use_mapping:
            maximum = None
            minimum = None
            for line in open(filepath):
                value = float(line.strip())
                if (maximum is None) or (maximum < value):
                    maximum = value
                if (minimum is None) or (minimum > value):
                    minimum = value

        line_index = 0
        for line in open(filepath):
            line_index += 1
            value = float(line.strip())
            if line_index not in result:
                result[line_index] = 0
            result[line_index] += weights[index] * (value - minimum) / (maximum - minimum)

    sum_weights = sum(weights)
    for index in result:
        print result[index] / sum_weights

if __name__ == '__main__':
    main()
