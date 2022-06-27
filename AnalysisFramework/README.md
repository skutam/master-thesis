# Analysis framework

The analysis is split into 5 parts:
 - `SimpleAnalysis` analyses the average distance between characters, first char occurrences,
    single char occurrences, password length occurrences and duo char occurrences
 - `CharacterClassAnalysis` analyses places the password into character classes based
on the characters they consist of,
 - `SequenceAnalysis` analyses the sequence of characters as they follow and the sequences on standard keyboard and numpad keyboard
 - `SubstringAnalysis` finds the substrings with the most occurrences,
 - `WordUseAnalysis` finds the words that have the most occurrences in the dataset.


## Directory structure
    .
    ├── credentials             # Database credentials 
    ├── datasets                # Dataset files with extension `txt`
    ├── analytical_output       # Output of analysis
    ├── src                     # Source files
    ├── scripts                 # Database scripts
    ├── tools                   # Folder for password guessers we are analysing
    ├── utilities               # Utilities
    ├── datasets_unique         # Generated folder of unique datasets
    ├── training_datasets       # Generated folder of training datasets
    |   ├── normal              # Generated folder of normal training datasets
    |   └── ascii               # Generated folder of ascii only training datasets
    ├── tmp                     # Generated folder of tmp files (will be removed after analysis finishes)
    ├── analyse.py              # Script for analysing password guessers
    ├── generate.py             # Script for generating training datasets
    └── README.md

## Installation

The analysis tool requires [Pip](https://pypi.org/project/pip/) to run. To install run:

```bash
$ apt install python3-pip	
```

After that we need to create an environment by typing in command 

```bash
$ python3 -m venv env
```

Then to use the environment we type in
```bash
$ source env/bin/activate
```

After that we will need to install the required libraries by typing 

```bash
$ pip3 install -r requirements.txt
```

## Usage

To run the analysis we need to specify which dataset we need to analyse by running the command

```bash
$ python3 analyse.py path_to_file
```

the result will be in the folder `analytical_framework/name_of_dataset`. Each result is in the form of `feature, count\n`.

### Generate training datasets

To generate training dataset we run command, when using the argument `--ascii` we will also generate the ASCII only dataset, when we want to rewrite already created training dataset we use `--rewrite`

```bash
$ python3 generate.py path_to_dataset [--ascii] [--rewrite]
```

the result will be in folder `training_datasets` and it will contain files `1m.txt`, `5m.txt`, `10m.txt` and `50m.txt` representing different sizes of training datasets.