from os import mkdir
from os.path import exists

import subprocess

from .AnalyticalFramework import SimpleAnalysis, WordUseAnalysis, SequenceAnalysis, CharacterClassAnalysis, \
    SubstringAnalysis
from .DatasetGenerators.Generator import generate_unique_datasets
from .utils import FONTCOLORS, get_dataset_name, constants


class Analysis:
    DATASET_PASSWORD_COUNT = 'dataset_password_count'

    def __init__(self):
        self._count_normal = 0
        self._count_unique = 0
        self._dataset = None
        self._dataset_name = None

    def _construct_folder_structure(self) -> None:
        """
            Construct dataset structure, for usage in analysis and for storing results

            Returns:
                None
        """
        # Create unique datasets
        if not exists(constants.UNIQUE_DATASET_FOLDER):
            mkdir(constants.UNIQUE_DATASET_FOLDER)

        # Create analytical output
        if not exists(constants.ANALYTICAL_OUTPUT):
            mkdir(constants.ANALYTICAL_OUTPUT)

        # Create dataset folder when one is missing
        if not exists(f'{constants.ANALYTICAL_OUTPUT}/{self._dataset_name}'):
            mkdir(f'{constants.ANALYTICAL_OUTPUT}/{self._dataset_name}')

    def _write_passwords_counts_in_file(self) -> None:
        # Save password counts into file
        with open(f'{constants.ANALYTICAL_OUTPUT}/{self._dataset_name}/{Analysis.DATASET_PASSWORD_COUNT}', 'w+')\
                as f_out:
            # Format string and save results
            head_string = ("Normal dataset count", "Unique dataset count")

            # Calculate maximum length for each column required
            width_col1 = max(len(str(self._count_normal)), len(head_string[0]))
            width_col2 = max(len(str(self._count_unique)), len(head_string[1]))

            # Format head row
            data_string = "{0:<{col1}}\t{1:>{col2}}\n" \
                .format(head_string[0], head_string[1],
                        col1=width_col1, col2=width_col2)

            # Format data rows
            data_string += "{0:<{col1}}\t{1:>{col2}}\n" \
                .format(self._count_normal, self._count_unique,
                        col1=width_col1, col2=width_col2)

            # Write string to file
            f_out.write(data_string)

    def _count_passwords_in_dataset(self) -> None:
        self._analysis = {}

        # Start counting the number of passwords of normal and unique datasets
        proc_normal = subprocess.Popen(['wc', '-l', self._dataset],
                                       stdout=subprocess.PIPE)
        proc_unique = subprocess.Popen(['wc', '-l', constants.UNIQUE_DATASET_FOLDER + '/' + self._dataset_name],
                                       stdout=subprocess.PIPE)

        # Wait for processes
        proc_normal.wait()
        proc_unique.wait()

        # Get number of passwords in normal dataset
        out, err = proc_normal.communicate()
        self._count_normal = out.decode("utf-8").split(' ')[0]

        # Get number of passwords in unique dataset
        out, err = proc_unique.communicate()
        self._count_unique = out.decode("utf-8").split(' ')[0]

    def run_analysis(self, file: str) -> None:
        """
            Run multiple analysis methods on dataset and then writes results into folder structure

            Returns
            -------
            None
        """
        # Get datasets from file/folder
        self._dataset = file
        self._dataset_name = get_dataset_name(file)

        # Create folder structure
        self._construct_folder_structure()

        # Create unique dataset
        print('Generating unique dataset')
        generate_unique_datasets(file)
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')


        # Instantiate analysis classes
        simple_analysis = SimpleAnalysis()
        word_use_analysis = WordUseAnalysis()
        substring_analysis = SubstringAnalysis()
        character_seq_analysis = SequenceAnalysis()
        character_class_analysis = CharacterClassAnalysis()

        # Count passwords for unique and normal datasets, and write results to file
        print('Counting passwords in dataset:')
        self._count_passwords_in_dataset()
        self._write_passwords_counts_in_file()
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        # Analyze each dataset with simple analysis
        print(f'Starting simple analysis')
        simple_analysis.analyse(self._dataset, self._count_unique)
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        # After simple analysis compute the classes, into which we will be dividing all the characters
        print(f'Generating character classes ', end='', flush=True)
        character_class_analysis.gen_char_classes(
            simple_analysis.get_char_list(),
            self._dataset_name,
            simple_analysis.get_highest_avg_char_dist()
        )
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        # Free memory from simple analysis, because we no longer need it
        simple_analysis.__del__()

        # Analyze each dataset with character sequence analysis
        print(f'Starting character sequence analysis')
        character_seq_analysis.analyse(self._dataset, self._count_unique)
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        print(f'Starting substring analysis')
        substring_analysis.analyse(self._dataset, self._count_unique)  # DONE
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        # Analyze each dataset with character class analysis
        print(f'Starting character class analysis')
        character_class_analysis.analyse(self._dataset, self._count_unique)
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')

        # Analyse each dataset with word use analysis
        print(f'Starting word use analysis')
        word_use_analysis.analyse(self._dataset, self._count_unique)
        print(f'{FONTCOLORS.GREEN}DONE{FONTCOLORS.CLEAR}')
