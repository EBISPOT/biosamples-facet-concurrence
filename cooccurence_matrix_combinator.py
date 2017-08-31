import json
import os
import re
from collections import Counter
from collections import Mapping
from pprint import pprint as pp

from operator import add

_FLAG_FIRST = object()


def flattenDict(d, join=add, lift=lambda x: x):
    results = []

    def visit(subdict, results, partial_key):
        for k, v in subdict.items():
            new_key = lift(k) if partial_key == _FLAG_FIRST else join(partial_key, lift(k))
            if isinstance(v, Mapping):
                visit(v, results, new_key)
            else:
                results.append((new_key, v))

    visit(d, results, _FLAG_FIRST)
    return results


if __name__ == "__main__":

    basename = 'cooccurrence_matrix\d+\.json'
    output_name = 'total_cooccurrence_matrix.json'
    files_folder = './'
    files = [f for f in os.listdir(files_folder) if re.match(basename, f)]

    final_matrix = Counter({})

    for f in files:
        print('Combining results from {}'.format(f))
        with open(f, 'r') as fin:
            partial_matrix = json.load(fin)
            partial_matrix_flatten = Counter(dict(flattenDict(partial_matrix, join=lambda a, b: a + '_' + b)))
            final_matrix += partial_matrix_flatten
        with open(output_name, 'w') as fout:
            json.dump(final_matrix, fout, sort_keys=True, indent=4)
