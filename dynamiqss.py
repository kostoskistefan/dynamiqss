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

    with open(dqss_file) as qss:
        for line in qss:
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
        value = split_variable[-1].replace(';', '')
        data[key] = value

    return data


def replace_variables():
    dictionary = create_dictionary()

    with open(dqss_file) as qss, open(qss_output_path, 'a') as output:
        dqss_text_block = False

        for line in qss:
            if variable_block_start in line:
                dqss_text_block = True

            elif variable_block_end in line:
                dqss_text_block = False
                continue

            if dqss_text_block:
                continue

            line_written = False

            for key, value in dictionary.items():
                if key in line:
                    output.write(line.replace(key, value))
                    line_written = True

            if not line_written:
                output.write(line)


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
