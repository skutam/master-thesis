from typing import Tuple, List

from src.utils import get_dataset_name

_DATASETS = ['000webhost', 'ClixSense', 'Crackstation', 'Mate1', 'Rambler', 'Twitter', 'VK_100M']
_TOOLS = ['John', 'OMEN', 'PCFG', 'Semantic guesser']


def get_datasets_bit_representation(datasets: List[str]) -> int:
    result = 0

    for dataset in datasets:
        try:
            index = _DATASETS.index(get_dataset_name(dataset))
        except ValueError:
            continue

        result = result | (1 << index)

    return result


class Password:
    def __init__(self, data: Tuple[str, int, int, int, int]):
        self._data = data

    def get_password(self):
        return self._data[0]

    def __str__(self):
        def _get_datasets(bit_datasets: int) -> str:
            datasets = []
            for n, dataset in enumerate(_DATASETS):
                if bit_datasets & (1 << n):
                    datasets.append(dataset)
            return ", ".join(datasets)

        def _get_tools(bit_tools: int) -> str:
            tools = []
            for n, tool in enumerate(_TOOLS):
                if bit_tools & (1 << n):
                    tools.append(tool)
            return ", ".join(tools)

        return """Password (
        password: {},
        count: {},
        dataset: {},
        tool: {},
        generated_dataset: {}
)""".format(self._data[0], self._data[1], _get_datasets(self._data[2]),
            _get_tools(self._data[3]), _get_datasets(self._data[4]))
