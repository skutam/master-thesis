from typing import Optional

from .state_saver import load_state, clear_state, save_state
from .hashes_state_saver import clear_hashes, load_hashes, add_found_hashes

from requests import get
from passlib.context import CryptContext

# Datasets we are working with
_DATASETS = {
    0x01: '000webhost',
    0x02: 'ClixSense',
    0x04: 'Crackstation',
    0x08: 'Mate1',
    0x10: 'Rambler',
    0x20: 'Twitter',
    0x40: 'VK_100M'
}


_SERVER_API = 'http://127.0.0.1:5000'


def _load_weak_hashes(_from: int, _limit: int) -> list:
    # Load _limit weak passwords from API
    r = get(f'{_SERVER_API}/passwords?from={_from}&limit={_limit}')
    data = r.json()
    return data['data']


def _create_weak_hash_results(_hash: tuple[str, Optional[str]],
                              weak_password_data: tuple) -> tuple[tuple[str, Optional[str]], int, list[str]]:
    # Generate the result structure we are returning
    datasets = [v for k, v in _DATASETS.items() if weak_password_data[2] & k]
    training_datasets = [v for k, v in _DATASETS.items() if weak_password_data[4] & k]

    if weak_password_data[3] != 0 and len(training_datasets) != 0:
        return {
            'identifier': _hash,
            'found_in_datasets': datasets,
            'severity': 'high',
            'training_datasets': training_datasets
        }
    return {
        'identifier': _hash,
        'found_in_datasets': datasets,
        'severity': 'medium'
    }


class Checker:
    LOAD_LIMIT = 1000

    def __init__(self, debug=False):
        # Initialize variables
        self._DEBUG: bool = debug
        self._state: Optional[dict] = None
        self._hashes: list[tuple[str, str]] = []
        self._ctx = CryptContext(schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14)

        # Load saved state
        self._load_saved_state()

    def _load_saved_state(self) -> None:
        # Load state from config file
        self._state = load_state()

        # No state saved, initialize new
        if self._state is None:
            self._state = {
                'from': 0
            }

        if self._DEBUG:
            print('Loaded saved state')
            print(f'Starting from {self._state["from"]}')

    def clear_old_session(self, keep_hashes=False) -> None:
        """
        Clear saved old session when we want to start from the start
        :param keep_hashes: Set to True when you want to skip hashes that were already cleared
        """
        clear_state()

        if keep_hashes:
            clear_hashes()

        if self._DEBUG:
            print('Cleared saved state and hashes.')

        # Reload state
        self._load_saved_state()

    def _clear_old_hashes(self) -> None:
        # Load hashes
        checked_hashes = load_hashes()

        hashes_count = len(self._hashes)

        # Filter out the hashes that we already checked
        self._hashes = list(filter(lambda _hash: _hash[0] not in checked_hashes, self._hashes))

        if self._DEBUG:
            print(f'Cleared out {hashes_count - len(self._hashes)} already checked hashes.')
            print(f'Working with {len(self._hashes)} unchecked hashes.')

    def load_passwords(self, hashes: Optional[list[str]] = None,
                       hashes_identities: Optional[list[tuple[str, str]]] = None) -> bool:
        """
        Add hashes to be cracked or hashes with identification to be returned
        :param hashes: List of hashes
        :param hashes_identities: List of tuples in a from of (hash, identification[email])
        :return: True when hashes were provided in valid structure, False otherwise
        """
        if hashes is None:
            hashes = []
        if hashes_identities is None:
            hashes_identities = []

        if len(hashes) == 0 and len(hashes_identities) == 0:
            if self._DEBUG:
                print('No hashes provided')
            return False

        # Load hashes
        if len(hashes) > 0:
            self._hashes = [(_hash, None) for _hash in hashes]

        # Load hashes with identities
        if len(hashes_identities) > 0:
            self._hashes.extend(hashes_identities)

        if self._DEBUG:
            print(f'Loaded {len(self._hashes)} passwords.')

        # Remove already checked hashes
        self._clear_old_hashes()
        return True

    def _filter_out_cleared_hashes(self, weak_hashes: list) -> None:
        # Check if hash is in the structure of weak hashes
        def _is_in(_hash: str) -> bool:
            for weak_hash in weak_hashes:
                if _hash == weak_hash['identifier'][0]:
                    return True
            return False

        # Filter out hashes we already checked
        self._hashes = [_h for _h in self._hashes if not _is_in(_h[0])]

    def check_next(self) -> Optional[list[tuple[tuple[str, Optional[str]], int, list[str]]]]:
        """
        Each call to this function tests the hashes against 100 000 weak passwords
        :return: None when there is nothing else to do, List of weak hashes found,
        ((hash, identity), count, list of datasets the hash has been found in)
        """
        # No more hashes to check ending
        if len(self._hashes) == 0:
            if self._DEBUG:
                print('No more hashes to check, ending.')
            return None

        if self._DEBUG:
            print(f'Loading {Checker.LOAD_LIMIT} weak passwords')
            print(f'Starting from index {self._state["from"]}.')

        # Load weak passwords
        weak_passwords = _load_weak_hashes(self._state["from"], Checker.LOAD_LIMIT)

        if self._DEBUG:
            print('Loading finished')

        weak_passwords_count = len(weak_passwords)

        # No more passwords to check ending
        if weak_passwords_count == 0:
            if self._DEBUG:
                print('No more weak passwords for checking, ending.')
            return None

        weak_hashes_found = []

        if self._DEBUG:
            print('Starting the finding of weak hashes ...')

        for i, weak_pass in enumerate(weak_passwords):
            if self._DEBUG:
                print(f'Weak passwords checked {i} from {weak_passwords_count}', end='\r')

            weak_hashes = []

            # Loop through hashes, and check each one against weak password
            for _hash in self._hashes:
                if self._ctx.verify(weak_pass[0], _hash[0]):
                    weak_hashes.append(_create_weak_hash_results(_hash, weak_pass))

            # Remove hashes we found
            self._filter_out_cleared_hashes(weak_hashes)

            # Append weak hashes found
            weak_hashes_found.extend(weak_hashes)

            # No more hashes left, ending
            if len(self._hashes) == 0:
                break
        
        print()

        # Update and save new state
        self._state['from'] += self.LOAD_LIMIT
        save_state(self._state)

        # Create list of hashes we found
        hashes_found = [h['identifier'][0] for h in weak_hashes_found]

        # Update file with found hashes
        add_found_hashes(hashes_found)

        # Return weak hashes that we found
        return weak_hashes_found
