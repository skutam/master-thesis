import subprocess
from os import mkdir
from os.path import exists
from shutil import rmtree
from typing import Dict
from math import ceil

from src.utils import get_dataset_name, constants

_MILLION = 1000000


def generate_unique_datasets(file: str) -> None:
    """
        Generate unique datasets for use in analysis

        Returns
        -------
        None
    """
    # When the file already exist, skip this part
    if exists(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(file)}'):
        return

    # Create unique datasets in parallel {sort | uniq > OUT.txt}
    with open(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(file)}', 'w+') as unique_dataset:
        # Generate unique dataset using {sort | uniq > unique_dataset}
        uniq_in = subprocess.Popen(['uniq', '-c'], stdin=subprocess.PIPE, stdout=unique_dataset).stdin
        subprocess.Popen(['sort', file], stdout=uniq_in).wait()


class Generator:
    def __init__(self):
        self._datasets = []

    def __del__(self):
        # Remove TMP folder after usage
        if exists(constants.TMP_FOLDER):
            rmtree(constants.TMP_FOLDER)

    def _construct_folder_structure(self):
        # Remove generated training datasets
        if exists(constants.TRAINING_DATASETS):
            rmtree(constants.TRAINING_DATASETS)

        if exists(constants.TMP_FOLDER):
            rmtree(constants.TMP_FOLDER)

        mkdir(constants.TRAINING_DATASETS)

        mkdir(constants.TMP_FOLDER)

        # Create folder for each dataset
        for dataset in self._datasets:
            mkdir(constants.TRAINING_DATASETS + '/' + get_dataset_name(dataset))

    def _get_dataset_counts(self) -> Dict[str, int]:
        counts = {}

        for dataset in self._datasets:
            # Create process to count passwords
            proc = subprocess.Popen(['wc', '/l', f'{constants.DATASET_FOLDER}/{dataset}'], stdout=subprocess.PIPE)
            proc.wait()

            # Get stdout and ignore stderr
            out, _ = proc.communicate()

            # Get count
            counts[dataset] = int(out.decode("utf-8").split(' ')[0])

        return counts

    def gen_random_training_dataset(self, dataset_sizes_m: list[int], dataset: str) -> None:

        pass

    def generate_random_training_datasets(self, dataset_sizes_m: list[int], datasets: list[str]) -> None:
        """
            Generate random training dataset from all the provided datasets

            Parameters
            ----------
            dataset_sizes_m: list[int]
                Dataset size in millions to be generated
            datasets: list[str
                List of datasets
            Returns
            -------
            None
        """
        self._datasets = datasets
        dataset_sizes = self._get_dataset_counts()

        # Sort required dataset sizes
        dataset_sizes_m.sort(reverse=True)

        # Skip other parts when this is empty
        if len(dataset_sizes_m) == 0:
            return

        # For each dataset generate TMP the highest number of dataset into tmp file
        for dataset in self._datasets:
            # We have enough passwords for generating training datasets
            if dataset in dataset_sizes and int(dataset_sizes[dataset]) > dataset_sizes_m[0] * _MILLION:
                with open(f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt', mode="w+") as tmp_dataset:
                    # Run bash script and wait for it to finish
                    subprocess.Popen(['bash', f'{constants.GEN_RANDOM_TRAINING_DATASET_SCRIPT}',
                                      f'{constants.DATASET_FOLDER}/{dataset}',
                                      f'{dataset_sizes_m[0] * _MILLION}'], stdout=tmp_dataset).wait()
                continue

            # Otherwise, we do not have enough data, concatenate the dataset X times
            with open(f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}_tmp.txt', mode="w+") as tmp_dataset:
                # Calculate the number of times we need to append dataset file into temporally file
                with open(f'{constants.DATASET_FOLDER}/{dataset}') as dataset_file:
                    # Append to file X times
                    for _ in range(ceil(dataset_sizes_m[0] * _MILLION / int(dataset_sizes[dataset]))):
                        dataset_file.seek(0)
                        tmp_dataset.write(dataset_file.read())

            with open(f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt', mode="w+") as tmp_dataset:
                # Run bash script and wait for it to finish
                subprocess.Popen(['bash', f'{constants.GEN_RANDOM_TRAINING_DATASET_SCRIPT}',
                                  f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}_tmp.txt',
                                  f'{dataset_sizes_m[0] * _MILLION}'], stdout=tmp_dataset).wait()

        for dataset in self._datasets:
            for dataset_size_m in dataset_sizes_m:
                with open(f'{constants.TRAINING_DATASETS}/{get_dataset_name(dataset)}/{dataset_size_m}m.txt', 'w+')\
                        as f_out:
                    subprocess.Popen(['head', f'{constants.TMP_FOLDER}/{get_dataset_name(dataset)}.txt',
                                      '-n', f'{dataset_size_m * _MILLION}'], stdout=f_out).wait()
