from os import listdir
from os.path import isfile
from pathlib import Path
from typing import List

from src.utils import constants


def gen_char_range(from_ch: str, to_ch: str) -> List[str]:
    """
        Function to generate list of characters from given character until given character (included)

        Parameters
        ----------
        from_ch: str
            Character from which we start generating
        to_ch: str
            Character until which we generate

        Returns
        -------
        List[str]
            List of generated characters
    """
    return [chr(x) for x in range(ord(from_ch), ord(to_ch) + 1)]


class FONTCOLORS:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CLEAR = '\033[0m'


def get_dataset_name(dataset: str) -> str:
    return Path(dataset).stem


def is_ascii_char(ch: str) -> bool:
    return ord('a') <= ord(ch) <= ord('z')


def is_number_char(ch: str) -> bool:
    return ord('0') <= ord(ch) <= ord('9')


def list_datasets() -> List[str]:
    # List files in dataset directory
    files = listdir(constants.DATASET_FOLDER)

    #
    return [file for file in files if isfile(f'{constants.DATASET_FOLDER}/{file}')]
