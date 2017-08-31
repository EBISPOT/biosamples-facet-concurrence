import re
import timeit
import string
import itertools
import json
import os

types_letter = list(string.ascii_lowercase)
types_letter.insert(0, "#")


def create_cooccurrence_matrix(params):

    in_filename = params['filename_in']
    out_filename = params['filename_out']
    # tcd = {letter: {} for letter in types_letter} # probably not necessary
    tcd = {}

    with open(in_filename, 'r') as f:
        samples_type_list = f.readlines()

    line_counter = 0
    total_lines = len(samples_type_list)
    for type_list in samples_type_list:
        if line_counter % 10 == 0:
            print('Line {} of {}'.format(line_counter, total_lines))
        types = [type_name.strip() for type_name in type_list.split(',') if type_name]
        types.sort()
        types_permutations = itertools.combinations(types, 2)
        for perm in types_permutations:
            (A, B) = perm
            # first_letter = str(A[0]).lower()
            # if first_letter not in string.ascii_lowercase:
            #     first_letter = "#"
            if A not in tcd:
                tcd[A] = {}

            if B not in tcd[A]:
                tcd[A][B] = 0

            tcd[A][B] += 1
        line_counter += 1

    with open(out_filename, 'w') as fout:
        json.dump(tcd, fout)

if __name__ == "__main__":

    # generate a dictionary to check if we already saw the type
    # Type check dictionary
    params = dict()

    base_filename_in = 'Thread\d_results.csv'
    base_filename_out = 'cooccurrence_matrix{}.json'

    input_files = [f for f in os.listdir('./') if re.match(base_filename_in, f)]
    for i in range(len(input_files)):
        input_file = input_files[i]
        print('Working on {}'.format(input_file))
        params['filename_in'] = input_file
        params['filename_out'] = base_filename_out.format(i+1)

        start_time = timeit.default_timer()
        create_cooccurrence_matrix(params)
        print(timeit.default_timer() - start_time)
