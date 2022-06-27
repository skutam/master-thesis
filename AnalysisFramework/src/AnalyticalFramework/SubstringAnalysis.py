from os import mkdir
from os.path import exists
from psutil import virtual_memory

from src.utils import constants, get_dataset_name


def _create_folder_struct(dataset: str) -> None:
    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SubstringAnalysis'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SubstringAnalysis')


class SubstringAnalysis:
    SUBSTRING_ANALYSIS = 'SubstringAnalysis'

    def __init__(self):
        self._substrings = {}
        self._substrings_index = 0
        self._dataset_name = None

    def _write_substring_dataset_analysis(self, dataset: str) -> None:
        # Save character frequency into file
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/{SubstringAnalysis.SUBSTRING_ANALYSIS}/{self._substrings_index}.txt', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._substrings.items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._substrings = {}
            
            # Write data to file
            for key, val in sorted_items:
                f_out.write(f'{key}, {val}\n')

            # Clear analysis and continue
            self._substrings_index += 1

    def _analyse_password(self, password: str, count: int) -> None:
        # Get all substrings of string
        res = [password[i: j] for i in range(len(password))
               for j in range(i + 1, len(password) + 1)]

        # Remove all words with length lower than 2
        res = [x for x in res if len(x) > 2]

        # Add substring to dictionary
        for substring in set(res):
            if substring not in self._substrings:
                self._substrings[substring] = count
            else:
                self._substrings[substring] += count

    def analyse(self, dataset: str, count_unique: int) -> None:
        # Clear analysis dictionary
        self._substrings = {}

        self._dataset_name = get_dataset_name(dataset)

        _create_folder_struct(self._dataset_name)

        i = 0

        # Analyse dataset line by line
        with open(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(dataset)}', encoding="utf-8") as dataset_file:
            for line in dataset_file:
                # Split values into the number of passwords and password
                count, password = line.lstrip().split(' ', 1)

                # Clear EOL
                password = password.rstrip('\n')

                # Skip invalid values
                if len(password) == 0:
                    continue

                # Analyse password
                self._analyse_password(password, int(count))
                
                # Write result when the memory is about to run out
                if float(virtual_memory()[2]) > 50.0:
                    print('\nWritting to file and clearing memory\n')
                    self._write_substring_dataset_analysis(self._dataset_name)
                
                print(f'{i}/{count_unique}', end='\r')
                i += 1
            print(f'{i}/{count_unique}')

        # Save analysis dictionary to file
        self._write_substring_dataset_analysis(dataset)
