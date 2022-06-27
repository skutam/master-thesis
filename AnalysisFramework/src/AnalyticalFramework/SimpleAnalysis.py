from os import mkdir
from os.path import exists
from typing import List

from src.utils import constants, get_dataset_name

MAX_PASS_LEN = 257


def _create_folder_struct(dataset: str) -> None:
    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SimpleAnalysis'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SimpleAnalysis')


class SimpleAnalysis:
    """
        Do simple analysis where we count the number of occurrences of first characters and duo of characters with
        password length distribution. With this analysis also construct the array of all characters that we have found
        in the datasets.
    """

    CHARACTER_FREQUENCY = 'character_frequency'
    CHARACTER_DUO_FREQUENCY = 'character_duo_frequency'
    PASSWORD_LENGTH = 'password_length'
    AVG_CHAR_DISTANCE = 'average_character_distance'
    FIRST_CHAR_FREQUENCY = 'first_char_frequency'

    def __init__(self):
        self._analysis = None
        self._chars_used = []
        self._average_char_distance = 0
        self._highest_avg_char_dist = 0
        
    def __del__(self):
        """
            Clear the enormous set of all the characters
        """
        self._chars_used = None

    def _analyse_single_character(self, password: str, count: int) -> None:
        """
            Count number of occurrences of characters in password

            Parameters
            ----------
            password: str
                Password for which we count the number of characters

            Returns
            -------
            None
        """
        for char in password:
            # Increment character
            if char in self._analysis[SimpleAnalysis.CHARACTER_FREQUENCY]:
                self._analysis[SimpleAnalysis.CHARACTER_FREQUENCY][char] += count
            else:
                self._analysis[SimpleAnalysis.CHARACTER_FREQUENCY][char] = count

            # Append to character list when not in
            if char not in self._chars_used:
                self._chars_used.append(char)

    def _analyse_character_duo(self, password: str, count: int) -> None:
        """
            Count number occurrences of character pairs in password

            Parameters
            ----------
            password: str
                Password for which we count the number of character pairs

            Returns
            -------
            None
        """
        # Loop through pairs of characters
        for i in range(len(password) - 1):
            duo = password[i:i + 2]

            # Increment character duo
            if duo in self._analysis[SimpleAnalysis.CHARACTER_DUO_FREQUENCY]:
                self._analysis[SimpleAnalysis.CHARACTER_DUO_FREQUENCY][duo] += count
            else:
                self._analysis[SimpleAnalysis.CHARACTER_DUO_FREQUENCY][duo] = count

    def _analyse_length(self, password: str, count: int) -> None:
        """
            Count the length distribution of passwords

            Parameters
            ----------
            password: str
                Password for which we count the length distribution

            Returns
            -------
            None
        """
        pass_len = len(password)

        if pass_len >= MAX_PASS_LEN:
            if pass_len in self._analysis[SimpleAnalysis.PASSWORD_LENGTH]:
                self._analysis[SimpleAnalysis.PASSWORD_LENGTH][pass_len] += count
            else:
                self._analysis[SimpleAnalysis.PASSWORD_LENGTH][pass_len] = count
        else:
            self._analysis[SimpleAnalysis.PASSWORD_LENGTH][pass_len] += count

    def _analyse_avg_len_of_chars(self, password: str, count: int) -> None:
        distance = 0

        for i in range(len(password) - 1):
            a, b = password[i:i+2]
            distance += abs(ord(a) - ord(b))

        # Skip
        if (len(password) - 1) == 0:
            return

        distance /= (len(password) - 1)
        distance = int(distance)

        # Calculate average char distance for splitting character classes
        self._average_char_distance += distance

        if distance in self._analysis[SimpleAnalysis.AVG_CHAR_DISTANCE]:
            self._analysis[SimpleAnalysis.AVG_CHAR_DISTANCE][distance] += count
        else:
            self._analysis[SimpleAnalysis.AVG_CHAR_DISTANCE][distance] = count

    def _analyse_first_char_frequency(self, password: str, count: int) -> None:
        if password[0] in self._analysis[SimpleAnalysis.FIRST_CHAR_FREQUENCY]:
            self._analysis[SimpleAnalysis.FIRST_CHAR_FREQUENCY][password[0]] += count
        else:
            self._analysis[SimpleAnalysis.FIRST_CHAR_FREQUENCY][password[0]] = count

    def _analyse_password(self, count: int, password: str) -> None:
        """
            Analyse each password using simple methods

            Parameters
            ----------
            password: str
                Password which we analyse using simple methods

            Returns
            -------
            None
        """
        # Analyse passwords
        self._analyse_single_character(password, count)
        self._analyse_character_duo(password, count)
        self._analyse_length(password, count)
        self._analyse_avg_len_of_chars(password, count)
        self._analyse_first_char_frequency(password, count)

    def _write_simple_dataset_analysis(self, dataset) -> None:
        """
            Write results of simple analysis into file

            Returns
            -------
            None
        """
        # Save character frequency into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/SimpleAnalysis/' + SimpleAnalysis.CHARACTER_FREQUENCY, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SimpleAnalysis.CHARACTER_FREQUENCY].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis[SimpleAnalysis.CHARACTER_FREQUENCY] = {}

            # Write string to file
            f_out.write(data_string)

        # Save duo character frequency into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/SimpleAnalysis/' + SimpleAnalysis.CHARACTER_DUO_FREQUENCY, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SimpleAnalysis.CHARACTER_DUO_FREQUENCY].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis[SimpleAnalysis.CHARACTER_DUO_FREQUENCY] = {}

            # Write string to file
            f_out.write(data_string)

        # Save password length distribution into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/SimpleAnalysis/' + SimpleAnalysis.PASSWORD_LENGTH, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SimpleAnalysis.PASSWORD_LENGTH].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis[SimpleAnalysis.PASSWORD_LENGTH] = {}

            # Write string to file
            f_out.write(data_string)

        # Save password length distribution into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/SimpleAnalysis/' + SimpleAnalysis.AVG_CHAR_DISTANCE, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SimpleAnalysis.AVG_CHAR_DISTANCE].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Get the distance that was most times found
            self._highest_avg_char_dist = sorted_items[0][0]

            # Clear out dictionary to free memory
            self._analysis[SimpleAnalysis.AVG_CHAR_DISTANCE] = {}

            # Write string to file
            f_out.write(data_string)

        # Save password length distribution into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/SimpleAnalysis/' + SimpleAnalysis.FIRST_CHAR_FREQUENCY, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SimpleAnalysis.FIRST_CHAR_FREQUENCY].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis[SimpleAnalysis.FIRST_CHAR_FREQUENCY] = {}

            # Write string to file
            f_out.write(data_string)

    def analyse(self, dataset: str, count_unique: int) -> None:
        """
            Analyse dataset line by line

            Parameters
            -----------
            dataset: string
                Name of dataset to be analyzed

            Returns
            -------
            None
        """
        # Initialise analysis dictionary
        self._analysis = {
            SimpleAnalysis.CHARACTER_FREQUENCY: {},
            SimpleAnalysis.CHARACTER_DUO_FREQUENCY: {},
            SimpleAnalysis.PASSWORD_LENGTH: {num: 0 for num in range(0, MAX_PASS_LEN)},
            SimpleAnalysis.AVG_CHAR_DISTANCE: {},
            SimpleAnalysis.FIRST_CHAR_FREQUENCY: {}
        }

        # Create simple analysis folder for dataset
        _create_folder_struct(dataset)

        # Analyse dataset line by line
        with open(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(dataset)}', encoding="utf-8") as dataset_file:
            password_count = 0
            i=0
            for line in dataset_file:
                # Split values into the number of passwords and password
                count, password = line.lstrip().split(' ', 1)

                # Clear EOL
                password = password.rstrip('\n')

                # Skip invalid values
                if len(password) == 0:
                    continue

                # Increment password counter
                password_count += int(count)

                # Analyse password
                self._analyse_password(int(count), password)
                print(f'{i}/{count_unique}', end='\r')
                i += 1
            print(f'{i}/{count_unique}')

        if password_count == 0:
            self._average_char_distance = 0
        else:
            self._average_char_distance = int(self._average_char_distance / password_count)

        # Save analysis dictionary to file
        self._write_simple_dataset_analysis(dataset)

    def get_char_list(self) -> List[str]:
        """
            Returns
            -------
            List[str] Set of characters found in dataset
        """
        return self._chars_used

    def get_highest_avg_char_dist(self) -> int:
        return self._highest_avg_char_dist
