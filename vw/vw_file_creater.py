import sys

def main():
    
    for line in sys.stdin:
        s = line.strip().split('\t')
        if s[1] == "0":
            s[1] = "-1"
        for i in xrange(len(s) - 2):
            s[i + 2] = "%s:%s" % (str(i + 1), s[i + 2])
        print "%s | %s" % (s[1], " ".join(map(str, s[2:])))

if __name__ == "__main__":
    main()