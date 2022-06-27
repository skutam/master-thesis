from os import mkdir
from os.path import exists
from typing import Tuple, Optional

from src.utils import constants, get_dataset_name

# Numpad keyboard keys
_NUMPADS = (
    (None, '/', '*', '-'),
    ('7', '8', '9', '+'),
    ('4', '5', '6', '+'),
    ('1', '2', '3', None),
    ('0', '0', ',', None)
)

# Keyboard keys
_KEYBOARD = (
    ('`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='),
    ('\t', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'),
    (None, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\'),
    (None, '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', None)
)


def _get_index(_list: Tuple, word: str) -> Optional[Tuple[int, int]]:
    """
        Get index of character in list

        Parameters
        ----------
        _list: Tuple
            List of lists containing keyboard or numpad characters

        Returns
        -------
        Optional[Tuple[int, int]]
            Return Tuple of indexes, or None when not found
    """
    for (i, sub_list) in enumerate(_list):
        if word in sub_list:
            return sub_list.index(word), i
    return None


def _is_neighbor(char_a: str, char_b: str, _list: Tuple) -> bool:
    """
        Check if char_b is neighbor of char_a

        Parameters
        ----------
        char_a: str
            Character one
        char_b: str
            Second character that may be neighbour of char_a
        _list: Tuple
            List representing keyboard

        Returns
        -------
        bool
            True when char_a is neighbor of char_b, False otherwise
    """
    # Get char_a index in list
    index = _get_index(_list, char_a)

    # Index not found, char_a has no neighbor
    if index is None:
        return False

    # Check all possible characters around char_a
    for x in range(-1, 2):
        for y in range(-1, 2):
            i = index[1] - x
            j = index[0] - y

            # When index is in range, check if char_b, is neighbor of char_a
            if 0 <= i < len(_list) and 0 <= j < len(_list[i]):

                # char_b is neighbour
                if _list[i][j] == char_b:
                    return True

    # char_b is not neighbour of char_a
    return False


def _create_folder_struct(dataset: str) -> None:
    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SequenceAnalysis'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/SequenceAnalysis')


class SequenceAnalysis:
    SEQUENCE_ANALYSIS = 'sequence_analysis'

    CHAR_ANALYSIS = 'char_analysis'
    KEYBOARD_ANALYSIS = 'keyboard_analysis'
    KEYBOARD_PATTERN_ANALYSIS = 'keyboard_pattern_analysis'
    NUMPAD_ANALYSIS = 'numpad_analysis'
    NUMPAD_PATTERN_ANALYSIS = 'numpad_pattern_analysis'

    def __init__(self):
        self._analysis = None

    def _analyse_pattern(self, string: str, _list: Tuple, analysis_name: str, count: int):
        sequence_index = []
        x, y = _get_index(_list, string[0])
        for char in string[1:]:
            _x, _y = _get_index(_list, char)
            sequence_index.append(f'{_x - x},{_y - y}')
            x = _x
            y = _y
        result = ' '.join(sequence_index)

        if result in self._analysis[analysis_name]:
            self._analysis[analysis_name][result] += count
        else:
            self._analysis[analysis_name][result] = count

    def _analyse_char_sequence(self, password: str, count: int) -> None:
        """
            Generate sequences of characters and add them to the dict

            Parameters
            ----------
            password: str
                String on which we count the sequence

            Returns
            -------
            None
        """
        seq = ''
        prev_char = None

        for i in range(len(password) - 1):
            a, b = password[i:i + 2]
            distance = abs(ord(b) - ord(a))

            # Characters in sequence
            if distance == 0 or distance == 1:
                seq += a
                prev_char = b
                continue

            # Prev char was ok, add to seq
            if prev_char is not None:
                seq += prev_char
                prev_char = None

            # Ignore empty or sequences of 2 or lower
            if seq == '' or len(seq) <= 2:
                seq = ''
                continue

            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.CHAR_ANALYSIS]:
                self._analysis[SequenceAnalysis.CHAR_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.CHAR_ANALYSIS][seq] = count

            seq = ''

        # Prev char was ok, add to seq
        if prev_char is not None:
            seq += prev_char

        # Ignore empty or sequences of 3 or lower
        if seq != '' and len(seq) > 2:
            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.CHAR_ANALYSIS]:
                self._analysis[SequenceAnalysis.CHAR_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.CHAR_ANALYSIS][seq] = count

    def _analyse_keyboard_sequences(self, password: str, count: int) -> None:
        """
            Analyse length of keyboard sequence

            Parameters
            ----------
            password: str
                Password to be analysed

            Returns
            -------
            None
        """
        seq = ''
        prev_char = None

        for i in range(len(password) - 1):
            a, b = password[i:i + 2]

            # Characters in sequence
            if _is_neighbor(a, b, _KEYBOARD):
                seq += a
                prev_char = b
                continue

            # Prev char was ok, add to seq
            if prev_char is not None:
                seq += prev_char
                prev_char = None

            # Ignore empty or sequences of 3 or lower
            if seq == '' or len(seq) <= 3:
                seq = ''
                continue

            # Add sequence vector to dict
            self._analyse_pattern(seq, _KEYBOARD, SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS, count)

            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS]:
                self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS][seq] = count

            seq = ''

        # Prev char was ok, add to seq
        if prev_char is not None:
            seq += prev_char

        # Ignore empty or sequences of 3 or lower
        if seq != '' and len(seq) > 3:
            # Add sequence vector to dict
            self._analyse_pattern(seq, _KEYBOARD, SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS, count)

            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS]:
                self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS][seq] = count

    def _analyse_numpad_sequences(self, password: str, count: int) -> None:
        """
            Analyse length of numpad sequences

            Parameters
            ----------
            password: str
                Password to be analysed

            Returns
            -------
            None
        """
        seq = ''
        prev_char = None

        for i in range(len(password) - 1):
            a, b = password[i:i + 2]

            # Characters in sequence
            if _is_neighbor(a, b, _NUMPADS):
                seq += a
                prev_char = b
                continue

            # Prev char was ok, add to seq
            if prev_char is not None:
                seq += prev_char
                prev_char = None

            # Ignore empty or sequences of 3 or lower
            if seq == '' or len(seq) <= 3:
                seq = ''
                continue

            # Add sequence vector to dict
            self._analyse_pattern(seq, _NUMPADS, SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS, count)

            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS]:
                self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS][seq] = count

            seq = ''

        # Prev char was ok, add to seq
        if prev_char is not None:
            seq += prev_char

        # Ignore empty or sequences of 3 or lower
        if seq != '' and len(seq) > 3:
            # Add sequence vector to dict
            self._analyse_pattern(seq, _NUMPADS, SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS, count)

            # Increment sequence length count
            if seq in self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS]:
                self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS][seq] += count
            # Sequence length count does not exist in dict, initialize new
            else:
                self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS][seq] = count

    def _write_sequence_analysis(self, dataset: str) -> None:
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/'
                  f'SequenceAnalysis/{SequenceAnalysis.CHAR_ANALYSIS}', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SequenceAnalysis.CHAR_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._analysis[SequenceAnalysis.CHAR_ANALYSIS] = {}

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Write string to file
            f_out.write(data_string)

        # Save keyboard sequence analysis
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/'
                  f'SequenceAnalysis/{SequenceAnalysis.KEYBOARD_ANALYSIS}', 'w+') as f_out:

            # Sort out dictionary
            sorted_items = list(self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._analysis[SequenceAnalysis.KEYBOARD_ANALYSIS] = {}

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Write string to file
            f_out.write(data_string)

        # Save keyboard pattern analysis
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/'
                  f'SequenceAnalysis/{SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS}', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._analysis[SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS] = {}

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Write string to file
            f_out.write(data_string)

        # Save keyboard sequence analysis
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/'
                  f'SequenceAnalysis/{SequenceAnalysis.NUMPAD_ANALYSIS}', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._analysis[SequenceAnalysis.NUMPAD_ANALYSIS] = {}

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Write string to file
            f_out.write(data_string)

        # Save keyboard pattern analysis
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/'
                  f'SequenceAnalysis/{SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS}', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Clear out dictionary to free memory
            self._analysis[SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS] = {}

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Write string to file
            f_out.write(data_string)

    def analyse(self, dataset: str, count_unique: int) -> None:
        # Initialize analysis dictionary
        self._analysis = {
            SequenceAnalysis.CHAR_ANALYSIS: {},
            SequenceAnalysis.KEYBOARD_ANALYSIS: {},
            SequenceAnalysis.KEYBOARD_PATTERN_ANALYSIS: {},
            SequenceAnalysis.NUMPAD_ANALYSIS: {},
            SequenceAnalysis.NUMPAD_PATTERN_ANALYSIS: {}
        }

        # Create folder structure
        _create_folder_struct(dataset)

        # Analyse dataset line by line
        with open(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(dataset)}', encoding="utf-8") as dataset_file:
            i = 0
            for line in dataset_file:
                # Split values into the number of passwords and password
                count, password = line.lower().lstrip().split(' ', 1)

                # Clear EOL
                password = password.rstrip('\n')

                # Skip invalid values
                if len(password) == 0:
                    continue

                # Analyse password for sequences
                self._analyse_char_sequence(password, int(count))
                self._analyse_keyboard_sequences(password, int(count))
                self._analyse_numpad_sequences(password, int(count))
                print(f'{i}/{count_unique}', end='\r')
                i += 1
            print(f'{i}/{count_unique}')

        # Save analysis dictionary to file
        self._write_sequence_analysis(dataset)
