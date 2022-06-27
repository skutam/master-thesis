from os import mkdir
from os.path import exists
from shutil import rmtree

from typing import List

from src.utils import constants, get_dataset_name


class Similarity:
    def __init__(self, datasets, training_dataset_indexes: List[int]):
        self._datasets = datasets
        self._training_dataset_indexes = training_dataset_indexes
        self._file_pointer = 0

        if not exists(constants.TMP_FOLDER):
            mkdir(constants.TMP_FOLDER)

    def split_datasets(self):
        if exists(f'{constants.TMP_FOLDER}/split_datasets'):
            rmtree(f'{constants.TMP_FOLDER}/split_datasets')
        mkdir(f'{constants.TMP_FOLDER}/split_datasets')

        for dataset in self._datasets:
            if not exists(f'{constants.TMP_FOLDER}/split_datasets/{get_dataset_name(dataset)}'):
                mkdir(f'{constants.TMP_FOLDER}/split_datasets/{get_dataset_name(dataset)}')

            with open(f'{constants.UNIQUE_DATASET_FOLDER}/{dataset}', encoding='utf-8') as f_d:
                count = 0
                i = 0
                f_out = None
                for line in f_d:

                    if i % 1000000 == 0:
                        if f_out is not None:
                            f_out.close()
                        f_out = open(f'{constants.TMP_FOLDER}/split_datasets/{get_dataset_name(dataset)}/{count}.txt',
                                     'w+', encoding='utf-8')
                        count += 1

                    f_out.write(line)
                    i += 1

                if f_out is not None:
                    f_out.close()

    def split_training_datasets(self):
        if exists(f'{constants.TMP_FOLDER}/split_training_datasets'):
            rmtree(f'{constants.TMP_FOLDER}/split_training_datasets')
        mkdir(f'{constants.TMP_FOLDER}/split_training_datasets')

        for dataset in self._datasets:
            for j in self._training_dataset_indexes:
                if not exists(f'{constants.TMP_FOLDER}/split_training_datasets/{get_dataset_name(dataset)}'):
                    mkdir(f'{constants.TMP_FOLDER}/split_training_datasets/{get_dataset_name(dataset)}')

                if not exists(f'{constants.TMP_FOLDER}/split_training_datasets/{get_dataset_name(dataset)}/{j}'):
                    mkdir(f'{constants.TMP_FOLDER}/split_training_datasets/{get_dataset_name(dataset)}/{j}')

                with open(f'{constants.TRAINING_DATASETS}/{get_dataset_name(dataset)}/{j}m.txt',
                          encoding='utf-8') as f_d:
                    count = 0
                    i = 0
                    f_out = None
                    for line in f_d:

                        if i % 1000000 == 0:
                            if f_out is not None:
                                f_out.close()
                            f_out = open(f'{constants.TMP_FOLDER}/split_training_datasets/{get_dataset_name(dataset)}/'
                                         f'{j}/{count}.txt', 'w+', encoding='utf-8')
                            count += 1

                        f_out.write(line)
                        i += 1

                    if f_out is not None:
                        f_out.close()
