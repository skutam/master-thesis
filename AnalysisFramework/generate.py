import argparse
import subprocess
import sys
from os import mkdir
from os.path import exists, isfile, dirname, join
from shutil import rmtree

from src.utils import constants, get_dataset_name, FONTCOLORS

_TRAINING_DATASET_SIZES = [1, 5, 10, 50]
_MILLION = 1000000
_DIRNAME = dirname(__file__)


def _construct_folder_structure():
    if not exists(constants.TRAINING_DATASETS):
        mkdir(constants.TRAINING_DATASETS)

    if not exists(constants.TRAINING_DATASETS_NORMAL):
        mkdir(constants.TRAINING_DATASETS_NORMAL)

    if not exists(constants.TRAINING_DATASETS_ASCII):
        mkdir(constants.TRAINING_DATASETS_ASCII)

    if not exists(constants.TMP_FOLDER):
        mkdir(constants.TMP_FOLDER)


def gen_training_dataset(dataset: str, rewrite: bool) -> bool:
    with open(f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt', mode="w+") as tmp_dataset:
        # Run bash script and wait for it to finish
        subprocess.Popen(['bash', f'{constants.GEN_RANDOM_TRAINING_DATASET_SCRIPT}',
                          f'{dataset}',
                          f'{_TRAINING_DATASET_SIZES[-1] * _MILLION}'], stdout=tmp_dataset).wait()

    # When it does not exist generate dataset folder
    if not exists(f'{constants.TRAINING_DATASETS_NORMAL}/{get_dataset_name(dataset)}'):
        mkdir(f'{constants.TRAINING_DATASETS_NORMAL}/{get_dataset_name(dataset)}')
    elif not rewrite:
        print('Dataset already exist, if you want to overide add argument --rewrite', file=sys.stderr)
        return False

    for dataset_size in _TRAINING_DATASET_SIZES:
        with open(f'{constants.TRAINING_DATASETS_NORMAL}/{get_dataset_name(dataset)}/{dataset_size}m.txt', 'w+')\
                as f_out:
            subprocess.Popen(['head', f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt',
                              '-n', f'{dataset_size * _MILLION}'], stdout=f_out).wait()

    return True


def gen_ascii_training_dataset(dataset: str, rewrite: bool):
    # When it does not exist generate dataset folder
    if not exists(f'{constants.TRAINING_DATASETS_ASCII}/{get_dataset_name(dataset)}'):
        mkdir(f'{constants.TRAINING_DATASETS_ASCII}/{get_dataset_name(dataset)}')
    elif not rewrite:
        print('Dataset already exist, if you want to overide add argument --rewrite', file=sys.stderr)
        return False
    
    for dataset_size in _TRAINING_DATASET_SIZES:
        with open(f'{constants.TRAINING_DATASETS_ASCII}/{get_dataset_name(dataset)}/{dataset_size}m.txt', 'w+')\
                    as f_out:
            # Run bash script and wait for it to finish
            subprocess.Popen(['bash', f'{constants.FILTER_ASCII_LINES_SCRIPT}',
                            f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt',
                            f'{dataset_size * _MILLION}'], stdout=f_out).wait()


def arguments() -> argparse.Namespace:
    """
        Parser arguments
    """
    parser = argparse.ArgumentParser(description='Generate from dataset unique datasets and training datasets')
    parser.add_argument('-f', '--file', required=True, help='Dataset file from which to generate training dataset')
    parser.add_argument('-r', '--rewrite', action='store_true', default=False, help='Rewrite already existing dataset')
    parser.add_argument('-a', '--ascii', action='store_true', help='Generate also ascii training datasets')
    return parser.parse_args()


if __name__ == '__main__':
    args = vars(arguments())

    file_path = join(_DIRNAME, args['file'])

    if not isfile(file_path):
        print('Given file not found', file=sys.stderr)
        exit(1)

    # Generate folder structure
    _construct_folder_structure()

    print('Generating training datasets')

    # Create and generate 
    if not gen_training_dataset(file_path, args['rewrite']):
        exit(1)
    print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

    if args['ascii']:
        print('Generating ascii only training datasets')
        gen_ascii_training_dataset(file_path, args['rewrite'])
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')
    
    # Remove TMP folder
    if exists(constants.TMP_FOLDER):
        rmtree(constants.TMP_FOLDER)
