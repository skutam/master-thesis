from os.path import realpath
from os import getcwd
import os

_constant_path = os.path.dirname(__file__)

DATASET_FOLDER = realpath(f'{getcwd()}/datasets')
UNIQUE_DATASET_FOLDER = realpath(f'{getcwd()}/datasets_unique')
ANALYTICAL_OUTPUT = realpath(f'{getcwd()}/analytical_output')
TRAINING_DATASETS = realpath(f'{getcwd()}/training_datasets')
TRAINING_DATASETS_NORMAL = realpath(f'{getcwd()}/training_datasets/normal')
TRAINING_DATASETS_ASCII = realpath(f'{getcwd()}/training_datasets/ascii')
TMP_FOLDER = realpath(f'{getcwd()}/tmp')

MOST_USED_WORDS = realpath(f'{getcwd()}/utilities/most_used_words')
GEN_RANDOM_TRAINING_DATASET_SCRIPT = realpath(f'{getcwd()}/utilities/gen_random_training_dataset.sh')
GEN_RANDOM_NON_UNIQUE_TRAINING_DATASET_SCRIPT = realpath(f'{getcwd()}/utilities'
                                                         f'/gen_random_non_unique_training_dataset.sh')
FILTER_ASCII_LINES_SCRIPT = realpath(f'{getcwd()}/utilities/filter_ascii_lines.sh')

DB_CONFIG = realpath(f'{getcwd()}/credentials/db.ini')
