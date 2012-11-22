#!/usr/bin/env python

from optparse import OptionParser
import logging
import os

_logger = logging.getLogger(__name__)

def shell_cmd(cmd):
    _logger.info(cmd)
    os.system(cmd)

def join_all_files(result_file, files_to_join):
    tmp_filepath = "dirty_tmp_file.never_used_2432"
    shell_cmd("rm -f %s; cp %s %s" % (result_file, files_to_join[0], result_file))
    for filepath in files_to_join[1:]:
        _logger.info("Joining %s" % filepath)
        os.system("paste %s %s > %s; mv %s %s" % (result_file, filepath, tmp_filepath, tmp_filepath, result_file))
    os.system("rm -f %s" % tmp_filepath)

def calc_script(result_file, script_filepath, data_file, arguments = None):
    _logger.info("Running %s script..." % script_filepath)
    os.system("rm -f %s" % result_file)
    if script_filepath.endswith(".py"):
        script_filepath = "python " + script_filepath
    if arguments is None:
        arguments = []
    shell_cmd("%s %s %s > %s" % (script_filepath, data_file, " ".join(arguments), result_file))
    return result_file

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE""")
    opts, args = optparser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    train_file = args[0]
    test_file = args[1]

    train_prefix = "train_"
    test_prefix = "test_"

    statistic_files = {
        "statistics_top_clicked_100_urls": "statistics_top_clicked_100_urls.tmp",
        "user_statistics": "user_statistics.tmp",
    }

    _logger.info("Calcing Statistics")
    calc_script(statistic_files["statistics_top_clicked_100_urls"], "statistics_top_clicked_urls.py", train_file, ["3 100 0.99985"])
    calc_script(statistic_files["user_statistics"], "statistics_user_info.py", train_file)


    feature_files = {
        "id_and_answer": "id_and_answer.tsv.tmp",
        "general_features": "general.tsv.tmp",
        "top_url": "top_url.tmp",
        "user_info": "user_info.tmp"
    }

    _logger.info("Generating id and answer column")
    calc_script(train_prefix + feature_files["id_and_answer"], "id_and_answer_calcer.py", train_file)
    calc_script(test_prefix + feature_files["id_and_answer"], "id_and_answer_calcer.py", test_file)

    _logger.info("Generating features")   
    _logger.info("Session Features")
    calc_script(train_prefix + feature_files["general_features"], "general_features.py", train_file)
    calc_script(test_prefix + feature_files["general_features"], "general_features.py", test_file)

    _logger.info("Statistic Features")
    calc_script(test_prefix + feature_files["top_url"], "top_urls_features.py", train_file, [statistic_files["statistics_top_clicked_100_urls"]])
    calc_script(train_prefix + feature_files["top_url"], "top_urls_features.py", test_file, [statistic_files["statistics_top_clicked_100_urls"]])

    _logger.info("User Features")
    calc_script(test_prefix + feature_files["user_info"], "user_info_features.py", train_file, [statistic_files["user_statistics"]])
    calc_script(train_prefix + feature_files["user_info"], "user_info_features.py", test_file, [statistic_files["user_statistics"]])

    _logger.info("File list building")
    train_files_to_join = [train_prefix + feature_files["id_and_answer"]]
    test_files_to_join = [test_prefix + feature_files["id_and_answer"]]
    for feature_name, feature_file in feature_files.iteritems():
        if feature_name != "id_and_answer":
            train_files_to_join.append(train_prefix + feature_file)
            test_files_to_join.append(test_prefix + feature_file)

    _logger.info("Joining features")
    join_all_files(train_prefix + "features.tsv", train_files_to_join)
    join_all_files(test_prefix + "features.tsv", test_files_to_join)

    _logger.info("Generating fml features_pool")
    shell_cmd("python convert_to_fml_features.py < " + train_prefix + "features.tsv > fml_" + train_prefix + "features.tsv")
    shell_cmd("python convert_to_fml_features.py < " + test_prefix + "features.tsv > fml_" + test_prefix + "features.tsv")
    _logger.info("Finished")

if __name__ == "__main__":
    main()
