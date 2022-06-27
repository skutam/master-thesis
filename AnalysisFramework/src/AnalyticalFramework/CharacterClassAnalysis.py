from os import mkdir
from os.path import exists
from typing import List

# List of whitespace characters
from src.utils import gen_char_range, get_dataset_name, constants

"""
    Got from
    https://documentation.softwareag.com/apama/v10-11/apama10-11/apama-webhelp/index.html#page/apama-webhelp/re-ApaEplRef_white_space.html
"""
WHITESPACE_CHARACTERS: List[str] = [
    chr(0x0020), chr(0x0009), chr(0x000c), chr(0x001c), chr(0x001d), chr(0x001e), chr(0x001f),          # ASCII
    chr(0x0085), chr(0x00a0), chr(0x1680), chr(0x180e), chr(0x2000), chr(0x2001), chr(0x2002),          # UTF-8
    chr(0x2003), chr(0x2004), chr(0x2005), chr(0x2006), chr(0x2007), chr(0x2008), chr(0x2009),
    chr(0x200a), chr(0x2028), chr(0x2029), chr(0x202f), chr(0x205f), chr(0x3000)
]

NON_PRINTABLE_CHARACTERS: List[str] = [ch for ch in gen_char_range(chr(0), chr(31)) if ch not in WHITESPACE_CHARACTERS]


def _create_folder_struct(dataset: str) -> None:
    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/CharacterClassAnalysis'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/CharacterClassAnalysis')

    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/CharacterClassAnalysis/char_classes'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/CharacterClassAnalysis/char_classes')


class CharacterClassAnalysis:
    CLASS_CHARACTER_ANALYSIS = 'class_character_analysis'
    CLASSES_FOLDER = 'char_classes'

    def __init__(self):
        self._analysis = {}
        self._classes: list[list[str]] = []
        self._division_classes = {}

    def gen_char_classes(self, character_list: List[str], dataset_name: str, char_distance: int) -> None:
        """
            Generate classes of characters that we will be matching against passwords

            Parameters
            ----------
            character_list: List[str]
                List of all characters we are working with
            dataset_name: str
                Name of dataset we are currently working with
            char_distance: int
                Character distance used for separating the characters

            Returns
            -------
            None
        """
        _create_folder_struct(dataset_name)

        # Add basic classes
        # Non-printable characters
        self._classes.append(NON_PRINTABLE_CHARACTERS)
        self._classes.append(WHITESPACE_CHARACTERS)     # Whitespace characters
        self._classes.append(gen_char_range('a', 'z'))
        self._classes.append(gen_char_range('A', 'Z'))
        self._classes.append(gen_char_range('0', '9'))
        self._classes.append([])

        for x in character_list:
            if len(x) > 1:
                for a in x:
                    print(f'{ord(a)} ', end='')
                print(x)

        # Sort list of characters by their int value
        character_list = sorted(character_list, key=lambda item: ord(item))

        print(char_distance)

        # Divide chars into classes from similar chunk of chars
        for char in character_list:
            # When last class is empty we add the character
            if len(self._classes[-1]) == 0:
                self._classes[-1].append(char)
                continue

            # When char is in one of the classes, we ignore it
            if max([int(char in class_chars) for class_chars in self._classes]) > 0:
                continue

            # When the difference between characters is higher than 1000, add to new class
            if abs(max([ord(x) for x in self._classes[-1]]) - ord(char)) > char_distance and \
               abs(min([ord(x) for x in self._classes[-1]]) - ord(char)) > char_distance:
                self._classes.append([char])
                continue

            # Add char to the last class
            self._classes[-1].append(char)

        # Sort each classes
        for i in range(len(self._classes)):
            self._classes[i] = sorted(self._classes[i], key=lambda item: ord(item))

        self._write_char_classes(dataset_name)

    def _write_char_classes(self, dataset_name: str) -> None:
        for i, _class in enumerate(self._classes):
            with open(f'{constants.ANALYTICAL_OUTPUT}/{dataset_name}/CharacterClassAnalysis/{self.CLASSES_FOLDER}/{i}',
                      'w+') as f_out:
                f_out.write("".join(_class))

    def _write_character_class_analysis(self, dataset: str) -> None:
        """
            Write analysis into file

            Parameters
            --------
            dataset: str
                Dataset of which analysis we are saving

            Returns
            -------
            None
        """
        # Save character frequency into file
        with open(constants.ANALYTICAL_OUTPUT + '/' + get_dataset_name(
                dataset) + '/CharacterClassAnalysis/' + CharacterClassAnalysis.CLASS_CHARACTER_ANALYSIS, 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis.items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis = {}

            # Write string to file
            f_out.write(data_string)

    def _analyse_password(self, password: str, count: int) -> None:
        """
            Analyse password

            Parameters
            ----------
            password: str
                Password which we are analysing
            count: int
                Number of times the same password has been found in dataset

            Returns
            -------
            None
        """
        classes = []

        for char in password:
            for i, _class in enumerate(self._classes):
                if char in _class:
                    classes.append(str(i))
                    break

        classes = list(set(classes))
        classes.sort()

        classes_str = ' '.join(classes)

        if classes_str in self._analysis:
            self._analysis[classes_str] += count
        else:
            self._analysis[classes_str] = count

    def analyse(self, dataset: str, count_unique: int) -> None:
        """
            Analyse each password of dataset

            Parameters
            ----------
            dataset: str
                Dataset file of which we are doing analysis

            Returns
            -------
            None
        """
        # Initialise analysis
        self._analysis = {}

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

                self._analyse_password(password, int(count))
                print(f'{i}/{count_unique}', end='\r')
                i += 1
            print(f'{i}/{count_unique}')

        # Save analysis dictionary to file
        self._write_character_class_analysis(dataset)
