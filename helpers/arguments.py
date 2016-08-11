import argparse
import constants as c

parser = argparse.ArgumentParser(description='This is ShevIT script by gromoleg.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-g', '--group', help='Group id', required=False,
                    default=c.DEFAULT_GROUP_ID)
parser.add_argument('-t', '--time', help='Update frequency in minutes', required=False,
                    default=c.DEFAULT_UPDATE_FREQUENCY, type=float)
parser.add_argument('--engine', help="Database engine to use", required=False,
                    default=c.DEFAULT_DB_ENGINE)
parser.add_argument('--migrate', help='Create tables in db and exit', required=False,
                    action='store_true')
