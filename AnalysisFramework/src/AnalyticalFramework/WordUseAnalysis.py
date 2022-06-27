from os import mkdir
from os.path import exists

from src.utils import constants, get_dataset_name, is_ascii_char

_CHAR_MAP = {
    'a': ('4', '/\\', '@', '/-\\', '^', '(L', 'Д'),
    'b': ('I3', '8', '13', '|3', 'ß', '!3', '(3', '/3', ')3', '|-]', 'j3', '6'),
    'c': ('[', '¢', '{', '<', '(', '©'),
    'd': (')', '|)', '(|', '[)', 'I>', '|>', '?', 'T)', 'I7', '|}', '>', '|]'),
    'e': ('3', '&', '£', '€', 'ë', '[-', '|=-'),
    'f': ('|=', 'ƒ', '|#', '/=', 'v'),
    'g': ('&', '6', '(_+', '9', 'C-', '(?,', '[,', '{,', '<-', '(.'),
    'h': ('#', '/-/', '[-]', ']-[', ')-(', '(-)', ':-:', '|~|', '|-|', ']~[', '}{', '!-!', '1-1', '\\-/', 'I+I', '/-\\'),
    'i': ('1', '[]', '|', '!', '3y3', ']['),
    'j': (',_|', '_|', '._|', '._]', '_]', ',_]', ']', ';', '1'),
    'k': ('>|', '|<', '/<', '1<', '|c', '|(', '|{'),
    'l': ('1', '£', '7', '|_', '|'),
    'm': ('/\\/\\', '/V\\', 'JVI', '[V]', '[]V[]', '|\\/|', '^^', '<\\/>', '{V}', '(v)', '(V)', '|V|', 'IVI', '|\\|\\', ']\\/[', '1^1', 'ITI', 'JTI'),
    'n': ('^/', '|\\|', '/\\/', '[\\]', '<\\>', '{\\}', '|V', '/V', 'И', '^', 'ท'),
    'o': ('0' , 'Q', '()', 'oh', '[]', '<>', 'Ø'),
    'p': ('|*', '|o', '|º', '?', '|^', '|>', '|"', '9', '[]D', '|°', '|7'),
    'q': ('(_,)', '9', '()_', '2', '0_', '<|', '&'),
    'r': ('I2', '|`', '|~', '|?', '/2', '|^', 'lz', '|9', '2', '12', '®', '[z', 'Я', '.-', '|2', '|-'),
    's': ('5', '$', '§', '2'),
    't': ('7', '+', '-|-', '\'][\'', '†', '"|"', '~|~'),
    'u': ('(_)', '|_|', 'v', 'L|', 'µ', 'บ'),
    'v': ('\\/', '|/', '\\|'),
    'w': ('\\/\\/', 'VV', '\\N', '\'//', '\\\\\'', '\\^/', '(n)', '\\V/', '\\X/', '\\|/', '\\_|_/', '\\_:_/', 'Ш', 'Щ', 'uu', '2u', '\\\\//\\\\//', 'พ', 'v²'),
    'x': ('><', 'Ж', '}{', '×', '?', ')(', ']['),
    'y': ('`/', 'Ч', '7', '\\|/', '¥', '\\//'),
    'z': ('2', '7_', '-/_', '%', '>_', '~/_', '-\\_', '-|_'),
}

_CHARS_MAX_CHAR_COUNT = max([len(x) for x in _CHAR_MAP.values()])


def _decode_leet_chars(password: str) -> str:
    """
        Replaces leet character representation for normal char

        Parameters:
        password: str
            Password which we will be replacing with characters

        Returns:
        str
            Password containing replaced characters
    """
    for i in range(0, _CHARS_MAX_CHAR_COUNT):
        for key in _CHAR_MAP:
            if i < len(_CHAR_MAP[key]):
                password = password.replace(_CHAR_MAP[key][i], key)
    return password


def _create_folder_struct(dataset: str) -> None:
    if not exists(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/WordUseAnalysis'):
        mkdir(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}/WordUseAnalysis')


class WordUseAnalysis:
    WORD_USES_ANALYSIS = 'word_use_analysis'

    def __init__(self):
        self._analysis = None
        self._leet_analysis = None
        self._words = []

        # Load words
        self._load_words()

    def _load_words(self) -> None:
        """
            Load most used words into List
        """
        with open(constants.MOST_USED_WORDS, 'r') as f:
            self._words = f.read().splitlines()

    def _write_word_use_dataset_analysis(self, dataset: str) -> None:
        """
            Save most common words usage into files

            Parameters
            ----------
            dataset: str
                Name of dataset

            Returns
            -------
            None
        """
        # Save character frequency into file
        with open(f'{constants.ANALYTICAL_OUTPUT}/{get_dataset_name(dataset)}'
                  f'/WordUseAnalysis/{WordUseAnalysis.WORD_USES_ANALYSIS}', 'w+') as f_out:
            # Sort out dictionary
            sorted_items = list(self._analysis[WordUseAnalysis.WORD_USES_ANALYSIS].items())
            sorted_items.sort(reverse=True, key=lambda item: item[1])

            # Format string and save results
            data_string = "".join(["{0}, {1}\n".format(key, val) for key, val in sorted_items])

            # Clear out dictionary to free memory
            self._analysis[WordUseAnalysis.WORD_USES_ANALYSIS] = {}

            # Write string to file
            f_out.write(data_string)

    def _analyse_password(self, password: str, leet_password: str, count: int) -> None:
        """
            Analyse given password

            Parameters
            ----------
            password: str
                Password to be analysed
            leet_password: str
                Password transformed using leet dictionary
            count: int
                Number of times the password has been found in the dataset

            Returns
            -------
            None
        """
        ascii_only_password = ''.join([ch for ch in password if is_ascii_char(ch)]).lower()
        ascii_only_leet_password = ''.join([ch for ch in leet_password if is_ascii_char(ch)]).lower()

        ascii_only_password_words = []
        ascii_only_leet_password_words = []

        pass_len = max(len(ascii_only_password), len(ascii_only_leet_password))

        for word in self._words:
            # End here, the words are longer than the password
            if len(word) > pass_len:
                break

            if word in ascii_only_password:
                ascii_only_password_words.append(word)

            if word in ascii_only_leet_password:
                ascii_only_leet_password_words.append(word)

        # Find the array with the most elements
        if len(ascii_only_leet_password_words) < len(ascii_only_password_words):
            words = ascii_only_password_words
        else:
            words = ascii_only_leet_password_words

        # Add each word into dist with count
        for word in words:
            if word in self._analysis[WordUseAnalysis.WORD_USES_ANALYSIS]:
                self._analysis[WordUseAnalysis.WORD_USES_ANALYSIS][word] += count
            else:
                self._analysis[WordUseAnalysis.WORD_USES_ANALYSIS][word] = count

    def analyse(self, dataset: str, count_unique: int) -> None:
        # Initialise analysis
        self._analysis = {
            WordUseAnalysis.WORD_USES_ANALYSIS: {}
        }

        _create_folder_struct(dataset)

        # Analyse dataset line by line
        with open(f'{constants.UNIQUE_DATASET_FOLDER}/{get_dataset_name(dataset)}', encoding="utf-8") as dataset_file:
            i = 0
            for line in dataset_file:
                # Split values into the number of passwords and password
                count, password = line.lstrip().split(' ', 1)

                # Remove EOL
                password = password.rstrip('\n')

                # Skip invalid values
                if len(password) == 0:
                    continue

                # Convert leet password, and analyse again
                leet_password = _decode_leet_chars(password)

                self._analyse_password(password, leet_password, int(count))
                print(f'{i}/{count_unique}', end='\r')
                i += 1
            print(f'{i}/{count_unique}')
        # Save analysis dictionary to file
        self._write_word_use_dataset_analysis(dataset)
