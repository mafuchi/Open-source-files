#!/usr/bin/env python3

#import whatever you need for yout demo
#ideally you woulnd't need anything
import csv

_author__ = "Michael Madden"
__copyright__ = "Copyright 2018, Michael Madden"
__license__ = "GPL"
__version__ = ".7"
__email__ = "mmadden.linguist@gmail.com"
__status__ = "Development"

#send the desired function to this module
def Demo_mode(_function):
    #set up logger to log
    logger = logging.getLogger(__name__)
    logger.info('This is a demo of the operation using a test set')
    #create the default demo foder
    if not os.path.exists('Demo_folder'):
        os.makedirs('Demo_folder')
    os.chdir('Demo_folder')

    '''
    creates a tsv file for demo to have CSV to TSV use to show how works
    Any other demo should have either an abilty to make a file so the demod
    funtion can be shown off, or just run the function with verbose logging
    '''
    with open('demo_set.tsv', 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        for i in range(5):
            writer.writerow(
                ['',randint(1, 100), randint(1, 100),'', randint(1, 100)])
    f.close()

    '''
    depending on what the out is needed by the funtion
    create a class to send back or just a var/dict
    '''
    class demo_set():
        extension ='tsv'
        input = None
        output = None
    #the name of the function
    _function(demo_set)

    logger.info(
    'This is a demo of the operation %s using a test set located in Demo_folder' % fun.__name__)
