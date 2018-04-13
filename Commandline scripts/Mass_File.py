#!/usr/bin/env python3

import sys
import os
import argparse
import re
import logging


_author__ = "Michael Madden"
__copyright__ = "Copyright 2018, Michael Madden"
__license__ = "GPL"
__version__ = ".9"
__email__ = "mmadden.linguist@gmail.com"
__status__ = "Development"

def mass_file(extension, folder_name=None, folder_location=None):
    logger = logging.getLogger(__name__)

    class return_object():
        def __init__(self, folder_location, files, folder_name):
            # to send off to other funcs
            self._folder_location = folder_location
            self._files = files
            self._folder_name = folder_name

    # finds the folder location indicated
    if folder_location is not None:
        os.chdir(folder_location)
    else:
        folder_location = os.getcwd()

    if folder_name is not None:
        chd_fld = folder_name
    else:
        folder_name = 'Test Folder'
        chd_fld = folder_name

    # makes a dir if the provided folder doesn't exist
    if not os.path.exists(chd_fld):
        os.makedirs(chd_fld)

    # add a dot if forgotten
    if re.match('\.', extension) is None:
        extension = '.' + extension

    # to check what is being fed
    logger.info('"%s" is the folder dir and "%s" is the folder name, with extention "%s"  ' %
                (folder_location, folder_name, extension))

    files = []
    for filename in os.listdir(os.getcwd()):
        # only takes the files with the correct extention
        # fixed to search insead of match
        if re.search(extension, filename):
            files.append(filename)
    # return list of file names
    logger.info("these are the files being processed " + str(files) + '\n')

    return return_object(folder_location, files, folder_name)


def Demo_mode(fun):
    logger = logging.getLogger(__name__)
    # put function name here
    # create files, read it and output for demo
    logger.info('creating a demo folder and files')
    if not os.path.exists('Demo_folder'):
        os.makedirs('Demo_folder')
    os.chdir('Demo_folder')
    for i in range(4):
        with open(str(i) + '_Demo.txt', 'w') as f:
            for i in range(10):
                f.write("this is line %d\r of the demo\n" % (i + 1))
    logger.info('Executing mass_file function')
    print('\n')
    mass_file('.txt')
    logger.info(
        'This is a demo of the operation %s using a test set located in Demo_folder' % fun.__name__)


def main():
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

    parser = argparse.ArgumentParser(description=('A script to to go through multiple files.'
                                                  'Please provide an extnesion, and optionally a folder name for the new files,'
                                                  'and a  folder location to find the files(current dir will be used otherwise)'))
    parser.add_argument('-e', '--extension',
                        help='Select the extention for your file')
    parser.add_argument(
        '-o', '--output', help='Select the file path for your output', required=False)
    parser.add_argument(
        '-i', '--input', help='Select the file path for your input(s)', required=False)
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

    #command line input logic
    while True:
        if (len(sys.argv) == 1) or ((arguments.verbose or arguments.log) is not None):
            try:
                test_response = input(
                    "\nPress Y to see a demo otherwise press N or Enter to exit\n")
                test_response = test_response.lower()
                pass
            except ValueError:
                logger.debug('Sorry, I did not understand that')
                continue
            if test_response in ['y', 'yes', 'yeah']:
                logger.debug('initiating Demo mode')
                Demo_mode(mass_file)
                break
            elif test_response in ['n', 'no', '']:
                logger.debug('...quiting')
                break
            else:
                logger.warning("You entered an unknown command, try again")
                continue
        elif len(sys.argv) > 1:
            logger.debug("these are the arguments givem %s", arguments)
            Mass_file(arguments.extension,
                          arguments.output, arguments.input)

if __name__ == "__main__":
    main()
