from optparse import OptionParser
import os
import logging
import random

_logger = logging.getLogger(__name__)

def shell_cmd(cmd):
    _logger.info(cmd)
    os.system(cmd)

def random_list(length):
    for i in xrange(length):
        p = random.random()
        if p < 0.90:
            yield i + 1

def convert_to_new_format(indexes, line):
    s = line.strip().split(' ')
    new_elms = list()
    for i in indexes:
        new_elms.append(s[i + 1])
    return "%s | %s\n" % (s[0], " ".join(map(str, new_elms)))

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FEATURES_FILE TEST_FEATURES_FILE""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    train_features_file = args[0]
    test_features_file = args[1]
    
    tmp_train_file_name = "new_train.tsv"
    tmp_test_file_name = "new_test.tsv"
    
    out_file_name = "outfile"
    
    tmp_predict_test_file = "predict_test"
    tmp_predict_train_file = "predict_train"

    predict_test_filename = "prediction_test_3.txt"
    predict_train_filename = "prediction_train_3.txt"

    prediction_test = [0] * 738997
    prediction_train = [0] * 7856735

    for iteration in xrange(20):
        fichaind = random_list(39)
        indexes = list(fichaind)
        
        train_features = open(train_features_file, 'rt')
        tmp_train_file = open(tmp_train_file_name, "w")
        try:
            for line in train_features:
                tmp_train_file.write(convert_to_new_format(indexes, line))
        finally:
            _logger.info("end_1_%s" % iteration)
            tmp_train_file.close()
            train_features.close()

        test_features = open(test_features_file, 'rt')
        tmp_test_file = open(tmp_test_file_name, "w")
        try:
            for line in test_features:
                tmp_test_file.write(convert_to_new_format(indexes, line))
        finally:
            _logger.info("end_1_%s" % iteration)
            tmp_test_file.close()
            test_features.close()

        vw = "%s\\%s" % (os.getenv("VOWPALWABBIT_HOME"), "vw.exe")
        shell_cmd("%s -d %s --loss_function logistic -f %s" % (vw, tmp_train_file_name, out_file_name))
        shell_cmd("%s -d %s --loss_function logistic -i %s -t -p %s" % (vw, tmp_test_file_name, out_file_name, tmp_predict_test_file))
        shell_cmd("%s -d %s --loss_function logistic -i %s -t -p %s" % (vw, tmp_train_file_name, out_file_name, tmp_predict_train_file))

        tmp_predict_test = open(tmp_predict_test_file, 'rt')
        try:
            i = 0
            for x in tmp_predict_test:
                prediction_test[i] += float(x)
                i += 1
        finally:
            _logger.info("end_2_%s" % iteration)
            tmp_predict_test.close()

        tmp_predict_train = open(tmp_predict_train_file, 'rt')
        try:
            i = 0
            for x in tmp_predict_train:
                prediction_train[i] += float(x)
                i += 1
        finally:
            _logger.info("end_3_%s" % iteration)
            tmp_predict_train.close()

    predict_test_file = open(predict_test_filename, "w")
    try:
        for x in prediction_test:
            predict_test_file.write(str(x / 20.0) + '\n')
    finally:
        _logger.info("end_test")
        predict_test_file.close()

    predict_train_file = open(predict_train_filename, "w")
    try:
        for x in prediction_train:
            predict_train_file.write(str(x / 20.0) + '\n')
    finally:
        _logger.info("end_train")
        predict_train_file.close()
        
if __name__ == "__main__":
    main()
