import sys

def main():
    files_to_combine = sys.argv[1:]
    result = {}

    for filepath in files_to_combine:
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
            result[index] += 1.0 * (value - minimum) / (maximum - minimum)

    for index in result:
        print result[index] / len(files_to_combine)

if __name__ == '__main__':
    main()
