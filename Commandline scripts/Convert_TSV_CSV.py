#!/usr/bin/env python3

# has to be run in py3 since py2 doesn't do unicode with csv files
from java_to_json import load_tag
from Mass_File import mass_file
from random import randint
import sys, logging
import os
import re
import json
import csv
import argparse


_author__ = "Michael Madden"
__copyright__ = "Copyright 2018, Michael Madden"
__license__ = "GPL"
__version__ = ".8"
__email__ = "mmadden.linguist@gmail.com"
__status__ = "Development"


def convert(arguments):
    logger = logging.getLogger(__name__)
    Mas_obj = mass_file(arguments.extension, arguments.output, arguments.input)
    if not os.path.exists('Demo_folder'):
        os.makedirs('Demo_folder')
    # the dict keys in use
    fieldnames = ('key_word', 'Tweet', 'Tw_ID')
    for old_file in Mas_obj._files:

        # open tsv file
        with open(old_file, 'r') as open_old_file:
            # change to the created folder
            os.chdir(Mas_obj._folder_location)

            # run the csv script on the tsv files
            # has to be open as file then read as csv
            # make it accept more than one ext

            working_old_file = csv.reader(open_old_file,
            delimiter='\t')
            logger.debug('the current file being processed %s  ', working_old_file)
            with open(Mas_obj._folder_name + '/' + old_file[:-3] + 'csv', 'w') as new_file:
                wtr = csv.writer(new_file)
                for row in working_old_file:
                    if len(row) == 5:
                        wtr.writerow((row[1], row[2], row[4]))

        new_file.close()
        open_old_file.close()
    # returns to the parent dir
    os.chdir('..')


def Demo_mode(fun):
    # create files, read it and output for demo
    logger = logging.getLogger(__name__)
    logger.info('This is a demo of the operation using a test set')
    if not os.path.exists('Demo_folder'):
        os.makedirs('Demo_folder')
    os.chdir('Demo_folder')
    with open('demo_set.tsv', 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        for i in range(5):
            writer.writerow(
                ['',randint(1, 100), randint(1, 100),'', randint(1, 100)])
    f.close()
    class demo_set():
        extension ='tsv'
        input = None
        output = None
    convert(demo_set)
    logger.info(
    'This is a demo of the operation %s using a test set located in Demo_folder' % fun.__name__)


def main(passed_args=None):
    #create logger
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(asctime)s %(name)s : %(levelname)s : \t %(message)s", "%d/%m/%Y %H:%M:%S")
    logger.setLevel(logging.DEBUG)

    #screen print out
    terminal_format = logging.Formatter("\n%(message)s")
    PR = logging.StreamHandler()
    PR.setLevel(logging.INFO)
    PR.setFormatter(terminal_format)
    logger.addHandler(PR)

    logger.debug('starting up...')

    parser = argparse.ArgumentParser(description=
    'A script to convert TSV files to CSV')
    parser.add_argument('-e', '--extension', help='Select the extention for your file', default='.tsv')
    parser.add_argument('-o','--output', help='Select the file path for your output', required=False)
    parser.add_argument('-i','--input', help= 'Select the file path for your input(s)',required=False)
    parser.add_argument("-v", "--verbose", help="show verbose logger", action="store_true")
    parser.add_argument("-l", "--log", help="log to file", action="store_true")

    arguments = parser.parse_args()

    #set the log levels
    if arguments.verbose:
        PR.setLevel(logging.DEBUG)
    elif arguments.log:
            logFilePath = "Mass_file.log"
            file_handler = logging.FileHandler(logFilePath)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)

    while True:
        if (len(sys.argv) == 1) or ((arguments.verbose or arguments.log) is not None):
            try:
                test_response = input(
                    "\nPress Y to see a demo otherwise press N or Enter to exit\n")
                test_response = test_response.lower()
                pass
            except ValueError:
                print ('Sorry, I did not understand that')
                continue

        if test_response in ['y', 'yes', 'yeah']:
            Demo_mode(convert)
            break
        elif test_response in ['n', 'no', '']:
            break


        elif len(sys.argv)==2:
            print ("\n\Optionally, please provide a folder name for the new files, and a  folder location to find the files(current dir will be used otherwise)\nOtherwise press Y or Enter to conitue")
            sys.exit(1)
        elif len(sys.argv)==3:
            print ("\n\tPlease provide the extenion \n")
            sys.exit(1)

    convert(arguments)

if __name__ == "__main__":
    main()
