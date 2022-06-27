from os import mkdir, remove
from os.path import dirname, realpath, exists

_cwd = dirname(__file__)
_CONFIG_FOLDER = realpath(f'{_cwd}/../config')
_HASHES_FILE = f'{_CONFIG_FOLDER}/hashes'


def add_found_hashes(hashes: list[str]) -> None:
    # When config folder does not exist create one
    if not exists(_CONFIG_FOLDER):
        mkdir(_CONFIG_FOLDER)

    # Open file and append hashes into it
    with open(_HASHES_FILE, 'a+') as f_out:
        f_out.write("\n".join(hashes))


def load_hashes() -> list[str]:
    # File does not exist, return empty array
    if not exists(_HASHES_FILE):
        return []

    # Open hashes file and convert to array of strings
    with open(_HASHES_FILE, 'r') as f_in:
        data = [line.rstrip() for line in f_in]

    # Return array of strings
    return data


def clear_hashes() -> None:
    if exists(_HASHES_FILE):
        remove(_HASHES_FILE)
