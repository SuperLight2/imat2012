#!/usr/bin/env python

from optparse import OptionParser
import os

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE """)
    opts, args = optparser.parse_args()

    for iteration in xrange(10):
        sub_train = 'sub_learn_%d' % iteration
        os.system('shuf -n 1000 < %s > %s' % (args[0], sub_train))
        os.system('python2.6 sklearn/sk_trainer.py -i 1 %s %s tmp prediction_test_%d.tsv' % (sub_train, args[1], iteration))
        os.system('rm -f %s' % sub_train)



if __name__ == '__main__':
    main()