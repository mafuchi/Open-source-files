#!/usr/bin/env python3

# has to be run in py3 since py2 doesn't do unicode with csv files
#from java_to_json import load_tag
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
    if arguments.input == 'demo':
        logger.info('demo Mass file being created')
        class Mas_demo():
            _folder_location = None
            _files = ['demo_set.tsv']
            _folder_name = 'Output_demo_folder'
            if not os.path.exists(_folder_name):
                os.makedirs(_folder_name)
        Mas_obj = Mas_demo

    else:
        Mas_obj = mass_file(arguments.extension, arguments.output, arguments.input)

    # the dict keys in use
    fieldnames = ('key_word', 'Tweet', 'Tw_ID')
    for old_file in Mas_obj._files:

        # open tsv file
        with open(old_file, 'r') as open_old_file:

            # run the csv script on the tsv files

            if re.match('.*\.tsv', old_file):
                logger.info('..tsv to csv')
                working_old_file = csv.reader(open_old_file,
                delimiter='\t')
                logger.debug('the current file being processed %s  ', old_file)
                with open(Mas_obj._folder_name + '/' + old_file[:-3] + 'csv', 'w', newline='') as new_file:
                    wtr = csv.writer(new_file)
                    for row in working_old_file:
                        to_output = []
                        for i in row:
                            #prints raw
                            logger.debug((repr(i)))
                            if i != '':
                                to_output.append(i)
                        logger.debug('%d items per row' %(len(to_output)))
                        wtr.writerow(to_output)

            #for CSV to JSON
            elif re.match('.*\.csv', old_file):
                logger.info('..csv to json')
                with open(open_old_file, 'r') as open_old_file:
                    reader = csv.DictReader(f, fieldnames)
                    # create count for rows to properly close json
                    row_count = sum(1 for row in reader)
                    # seek back to begining of file, so it can be read for writing
                    open_old_file.seek(0)
                    logger.info(row_count)
                    logger.debug('the current file being processed %s  ', old_file)
                    i = 0
                    with open(path + '/' + _file[:-3] + 'json', 'w') as new_file:
                        new_file.write('[\n')
                        for row in reader:
                            json.dump(row, j)
                            i += 1
                            if i != (row_count):
                                new_file.write(',\n')
                            else:
                                new_file.write('\n]')


        new_file.close()
        open_old_file.close()
    # returns to the parent dir
    os.chdir('..')


def Demo_mode():
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
    logger.debug('demo tsv file being created')
    class demo_set():
        extension ='tsv'
        input = 'demo'
        output = None
    convert(demo_set)
    logger.info(
    'This is a demo of the operation "%s" using a test set located in Demo_folder' % convert.__name__)


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
            Demo_mode()
            break
        elif test_response in ['n', 'no', '']:
            break
        else:
            convert(arguments)

if __name__ == "__main__":
    main()
