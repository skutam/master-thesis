# Reactive-password-checker

Reactive password checker is a tool for finding weak hashes in your databases. It detects weak hash and reports the number of times it has been found in leaked databases and lists all the databases it has been found in.

## Installation

Reactive-password-checker requires [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/stable/installation/) to run.

```bash
$ apt-get install python3.8
$ apt-get install python3-pip
```

It is recommended to create a environment and install the packages there, with commands:

```bash
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

## Usage

```python
from pprint import pprint

from ReactivePasswordChecker import Checker
from passlib.context import CryptContext

# List of weak passwords
passwords = [
    '123456',
    'asdasd',
    '123456789',
    '000000',
    'qwerty',
    '123456',
    'asdasd',
    '123456789',
    '000000',
    'qwerty'
]

# Generate array of hashed passwords or load from database
ctx = CryptContext(schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=10)
hashed_passwords = [ctx.hash(p) for p in passwords]

# Initialize checker and load hashed passwords
checker = Checker(True)
checker.load_passwords(hashed_passwords)

# Clear old session if you want to start from the start
checker.clear_old_session()     

# Keep checking with weak passwords, 10 000 per one run of check_next
while True:
    weak_hashes = checker.check_next()

    # Ending
    if weak_hashes is None:
        break

    pprint(weak_hashes)

```