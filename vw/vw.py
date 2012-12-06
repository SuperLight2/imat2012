from optparse import OptionParser
import sys
import os
import logging
import random

_logger = logging.getLogger(__name__)

def shell_cmd(cmd):
    _logger.info(cmd)
    os.system(cmd)

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FEATURES_FILE TEST_FEATURES_FILE""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    train_features_file = args[0]
    test_features_file = args[1]
    
    out_file_name = "outfile"
    
    predict_test_filename = "prediction_test_x.txt"
    predict_train_filename = "prediction_train_x.txt"
    
    vw_path = os.getenv("VOWPALWABBIT_HOME")
    print vw_path
    vw = "%s\\%s" % (os.getenv("VOWPALWABBIT_HOME"), "vw.exe")
    shell_cmd("%s -d %s --loss_function logistic -f %s" % (vw, train_features_file, out_file_name))
    shell_cmd("%s -d %s --loss_function logistic -i %s -t -p %s" % (vw, test_features_file, out_file_name, predict_test_filename))
    shell_cmd("%s -d %s --loss_function logistic -i %s -t -p %s" % (vw, train_features_file, out_file_name, predict_train_filename))
    
if __name__ == "__main__":
    main()
