from os import mkdir, remove
from os.path import dirname, realpath, exists
import pickle
from typing import Union

_cwd = dirname(__file__)
_CONFIG_FOLDER = realpath(f'{_cwd}/../config')
_STATE_FILE = f'{_CONFIG_FOLDER}/state'


def save_state(data: dict) -> None:
    # When config folder does not exist create one
    if not exists(_CONFIG_FOLDER):
        mkdir(_CONFIG_FOLDER)

    with open(_STATE_FILE, 'wb') as f_out:
        pickle.dump(data, f_out)


def load_state() -> Union[None, dict]:
    if not exists(_STATE_FILE):
        return None

    with open(_STATE_FILE, 'rb') as f_in:
        data = pickle.load(f_in)

    return data


def clear_state():
    if exists(_STATE_FILE):
        remove(_STATE_FILE)
