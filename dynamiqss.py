#! /usr/bin/python3

import os
import argparse

dqss_file = ""
qss_output_path = ""

variable_block_start = '@variables'
variable_block_end = '@endvariables'


def read_variables():
    data = []
    readingInProgress = False

    with open(dqss_file) as dqss:
        for line in dqss:
            if variable_block_end in line:
                readingInProgress = False
            if readingInProgress:
                data.append(line.strip())
            if variable_block_start in line:
                readingInProgress = True

    return data


def create_dictionary():
    data = {}

    for variable in read_variables():
        split_variable = variable.split(':')
        key = split_variable[0]
        value = split_variable[-1].replace(';', '').strip()
        data[key] = value

    return data


def replace_variables():
    dictionary = create_dictionary()

    with open(dqss_file) as dqss, open(qss_output_path, 'w') as output:
        dqss_text_block = False

        for line in dqss:
            if variable_block_start in line:
                dqss_text_block = True

            elif variable_block_end in line:
                dqss_text_block = False
                continue

            if dqss_text_block:
                continue

            current_line = line

            for key, value in dictionary.items():
                if key in current_line:
                    current_line = current_line.replace(key, value)

            output.write(current_line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile dqss to qss file')
    parser.add_argument('-i', '--input', required=True, help='Path to the source dqss file')
    parser.add_argument('-o', '--output', required=True, help='Output path for the compiled qss file')

    args = parser.parse_args()

    if not args.input.lower().endswith('.dqss'):
        raise ValueError("Input source file must a dqss file.")

    dqss_file = args.input
    qss_output_path = args.output
 
    if not qss_output_path.endswith('.qss'):
        filename = os.path.basename(dqss_file)
        output_file = os.path.splitext(filename)[0] + '.qss'
        qss_output_path = qss_output_path + output_file
    
    replace_variables()
