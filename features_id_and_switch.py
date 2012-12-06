#!/usr/bin/env python

from optparse import OptionParser

from tools.id_and_switch_calcer import SessionIdAndSwitchFeatureCalcer
from tools.session_reader import SessionReader

def main():
    optparser = OptionParser(usage="""
            %prog [OPTIONS] TRAIN_FILE TEST_FILE""")
    optparser.add_option('-d', '--description', dest='description_file',
        metavar='FILE', type='string', default=None,
        help='filepath for features description')
    opts, args = optparser.parse_args()

    session_id_and_switch_calcer = SessionIdAndSwitchFeatureCalcer()
    for session in SessionReader().open(args[0]):
        print "\t".join(map(str, session_id_and_switch_calcer.calc_features(session)))
    if opts.description_file is not None:
        output_file = open(opts.description_file, 'w')
        print >> output_file, "\n".join(map(str, session_id_and_switch_calcer.get_description()))
        output_file.close()

if __name__ == "__main__":
    main()

