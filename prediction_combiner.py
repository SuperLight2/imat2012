import sys

def try_to_float(s):
    try:
        value = float(s)
    except ValueError:
        return False, 0
    return True, value

def main():
    files_to_combine = []
    weights = []

    current_weight = 1.0
    for filepath in sys.argv[1:]:
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
        maximum = None
        minimum = None
        for line in open(filepath):
            value = float(line.strip())
            if (maximum is None) or (maximum < value):
                maximum = value
            if (minimum is None) or (minimum > value):
                minimum = value

        index = 0
        for line in open(filepath):
            index += 1
            value = float(line.strip())
            if index not in result:
                result[index] = 0
            result[index] += weights[index] * (value - minimum) / (maximum - minimum)

    sum_weights = sum(weights)
    for index in result:
        print result[index] / sum_weights

if __name__ == '__main__':
    main()
