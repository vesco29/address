#!/usr/bin/env python

import argparse
import pathlib
import os

from src.app import Selector

HOME = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser(description='Given a csv file contained people and their addresses and create output file that groups people who live at the same address.')

parser.add_argument('-i','--input' ,  type=pathlib.Path, required=True,
                    help='input path to csv file containing people and their addresses')
parser.add_argument('-o','--output' ,  type=pathlib.Path, default=HOME,
                    help='output path to write file (default: %(default)s)  ')
parser.add_argument('-f','--output-file-name' , default='sorted.csv',
                    help='output file name (default: %(default)s)  ')

args = parser.parse_args()

if __name__ == '__main__':
    print(args)
    print(os.path.isfile(args.input))
    output_file = os.path.join(args.output, args.output_file_name)
    print(f"Output file {output_file}")
    select = Selector(args.input, output_file)
    select.create_out_file()