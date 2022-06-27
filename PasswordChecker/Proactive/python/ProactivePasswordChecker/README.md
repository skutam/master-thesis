# Proactive-password-checker

Proactive password checker is a tool for finding weak passwords, by calculating the similarity rate with a weak dataset
we produced.

## Installation

Proactive-password-checker requires [Python](https://www.python.org/downloads/) to run.

```bash
$ apt-get install python3
```

## Usage

```Python
from pprint import pprint
from skutam import validate_password

threshold = 0.225

result = validate_password('password')

pprint(result)

if result['result'] < threshold:
    print('Password is strong')
else:
    print('Password is weak')

```