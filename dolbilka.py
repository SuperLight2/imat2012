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
        "statistics_top_clicked_100_urls": "statistics.top_clicked_100_urls",
        "user_statistics": "statistics.users",
    }

    _logger.info("Calcing Statistics")
    calc_script(statistic_files["statistics_top_clicked_100_urls"], "statistics_top_clicked_urls.py", train_file, ["3 100 0.99985"])
    calc_script(statistic_files["user_statistics"], "statistics_user_info.py", train_file)

    features_groups = {
        "id_and_answer": "group.id_and_answer",
        "general_features": "group.general_features",
        "top_url": "group.top_url",
        "user_info": "group.user_info"
    }

    feature_files = {
        features_groups["id_and_answer"]: "features.id_and_answer",
        features_groups["general_features"]: "features.general_features",
        features_groups["top_url"]: "features.top_url",
        features_groups["user_info"]: "features.user_info"
    }
    features_description_file = {
        features_groups["id_and_answer"]: "description.id_and_answer",
        features_groups["general_features"]: "description.general_features",
        features_groups["top_url"]: "description.top_url",
        features_groups["user_info"]: "description.user_info"
    }

    _logger.info("Generating id and answer column")
    calc_script(train_prefix + feature_files[features_groups["id_and_answer"]], "features_id_and_switch.py", train_file,
        ["-d " + features_description_file[features_groups["id_and_answer"]]])
    calc_script(test_prefix + feature_files[features_groups["id_and_answer"]], "features_id_and_switch.py", test_file)

    _logger.info("Generating features")
    _logger.info("Session Features")
    calc_script(train_prefix + feature_files[features_groups["general_features"]], "features_session_general.py", train_file,
        ["-d " + features_description_file[features_groups["general_features"]]])
    calc_script(test_prefix + feature_files[features_groups["general_features"]], "features_session_general.py", test_file)

    _logger.info("Statistic Features")
    calc_script(train_prefix + feature_files[features_groups["top_url"]], "features_top_urls.py", train_file,
        [statistic_files["statistics_top_clicked_100_urls"], "-d " + features_description_file[features_groups["top_url"]]])
    calc_script(test_prefix + feature_files[features_groups["top_url"]], "features_top_urls.py", test_file,
        [statistic_files["statistics_top_clicked_100_urls"]])

    _logger.info("User Features")
    calc_script(train_prefix + feature_files[features_groups["user_info"]], "features_users_info.py", train_file,
        [statistic_files["user_statistics"], "-d " + features_description_file[features_groups["user_info"]]])
    calc_script(test_prefix + feature_files[features_groups["user_info"]], "features_users_info.py", test_file,
        [statistic_files["user_statistics"]])

    _logger.info("File list building")
    train_files_to_join = [train_prefix + feature_files[features_groups["id_and_answer"]]]
    test_files_to_join = [test_prefix + feature_files[features_groups["id_and_answer"]]]
    features_description_files = [features_description_file[features_groups["id_and_answer"]]]
    for features_group in features_groups:
        if features_groups != "id_and_answer":
            train_files_to_join.append(train_prefix + feature_files[features_groups[features_group]])
            test_files_to_join.append(test_prefix + feature_files[features_groups[features_group]])
            features_description_files.append(features_description_file[features_groups[features_group]])

    result_file = "features.tsv"
    _logger.info("Joining features")
    join_all_files(train_prefix + result_file, train_files_to_join)
    join_all_files(test_prefix + result_file, test_files_to_join)

    _logger.info("Joining descriptions")
    description_file = "description.features.tsv"
    os.system("rm -f %s" % description_file)
    os.system("touch %s" % description_file)
    for filepath in features_description_files:
        os.system("cat %s >> %s" % (filepath, description_file))
        os.system("rm -f %s" % filepath)

    _logger.info("Generating fml features_pool")
    shell_cmd("python convert_to_fml_features.py < " + train_prefix + result_file + " > fml_" + train_prefix + result_file)
    shell_cmd("python convert_to_fml_features.py < " + test_prefix + result_file + " > fml_" + test_prefix + result_file)
    _logger.info("Finished")

if __name__ == "__main__":
    main()
