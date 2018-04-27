#!/usr/bin/env python3

import json
import subprocess
import codecs
import os
import shutil
import re

_author__ = "Michael Madden"
__copyright__ = "Copyright 2017, Michael Madden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "mmadden.linguist@gmail.com"
__status__ = "Development"


def load_tag(infile, path=None, outfile=None, keys=None, to_tag=None):
    logger = logging.getLogger(__name__)

    # if input data is not json, convert to json_data
    if re.match('.*\.json', infile.lower()) is None:
        if re.match('.*\.tsv', infile.lower()):
            new_infile = convert(infile)
            infile = convert(new_infile)
        elif:
            re.match('.*\.csv', infile.lower()):
            infile = convert(infile)
    #create a path if none is given
    if path = None:
        path = os.gcwd()
        #create a path from the input
    logger.debug('Path is %s' % path)

    #create a outfile if none is given
    if outfile = None:
        outfile = str(infile[:-4]) + '_tagged.json'
    logger.debug('outfile is %s' % outfile)

    #temp list to dump convert json data
    data_file = []

    with open(infile, 'r') as json_data, open(outfile, 'w') as f:
        if not os.path.exists('./temp/'):
            logger.info('creating temp folder')
            os.mkdir('./temp/')
        json_file = json.load(json_data)
        json_data.close()
        f.write('[\n')
        '''
        create a list to be used in conjugction with the
        labels list to create dictionaires for tagging tweet
        to be used for the tagged tweet
        '''
        if keys = None:
            keys = ['Word_order', 'Word', 'POS', 'Probability']
        logger.debug('using the keys %s' % keys)

        for i in json_file:
            # to set the order of the the tagged item
            tagged_count = 0
            temp_file = open('./temp/temp_file.txt', 'w')

            # takes the tweet in the JSON object
            # (i["key_word"]) for a specific dict
            if to_tag is None:
                temp = (i[u"Tweet"])
            elif 'pos' not in to_tag:
                to_tag.append('pos')
            else:
                #to make it read the item corrctly
                temp = (i['u"'+str(to_tag)+'"'])
            logger.debug('JSON object to tag "%s"' % temp)

            temp_file.write((temp))
            temp_file.close()

            # option output to show sentences being parsed
            logger.debug('loading json file %s to be read from temp' % infile)
            with codecs.open('./temp/temp_file.txt', "r", encoding='utf-8', errors='ignore') as fdata:
                for p in fdata:
                    logging.info(str(p))
            fdata.close()

            # take the java program and have it run
            # line by line tweets
            with open('./temp/temp_file2.txt', 'w') as g:
                logger.debug(
                    'creating temp file and running the sdout logger for JSON parser')
                #CMU Ark Twitter POS tagger used
                #https://github.com/brendano/ark-tweet-nlp
                subprocess.call(['java', '-jar', '../ark-tweet-nlp-0.3.2.jar',
                                 '--output-format', 'conll', './temp/temp_file.txt'],
                                stdout=g)
            g.close()

            # open the created temp file to check it is saving the parsed tweet
            with open('./temp/temp_file2.txt', 'r') as sdata:
                logger.debug(
                    'opening temp file2 of %s to create dicts ' % infile)
                Dicts = []
                # create a dictionary from the output
                for q in sdata:
                    values = []
                    tagged_count += 1  # for word order
                    values.append(tagged_count)
                    q = q.rstrip()
                    values = values + (q.split('\t'))
                    dictionairy = dict(zip(keys, values))
                    Dicts.append(dictionairy)
                    i.update({'Tagged': Dicts})  # append dictionaries to tweet
                    tweetPOS = []  # collect all the POS for each tweet and make a new entry
                    for word in i['Tagged']:
                        # incase there is a null obj attached
                        try:
                            #this would have to be changed if you changed keys
                            tweetPOS.append(word['POS'])
                        except:
                            pass

                    # after the while statement has finished join the POS of the sentence
                    h = ' '.join(tweetPOS)

                    # add the new POS to the list of sentences
                    i.update({'POS_S': h})

                sdata.close()

            # create an output file
            data_file.append(i)
        logger.debug('dumping object to file')
        json.dump(data_file, f, indent=1)
        # add the end brackets to the file to be valid JSON.
        f.write('\n]')
    # remove temp files

    shutil.rmtree('./temp/')
    f.close()
    logger.info('...removing temp folder')


def convert(old_file):
    logger = logging.getLogger(__name__)
    fieldnames = ('key_word', 'Tweet', 'Tw_ID')

    if re.match('.*\.tsv', old_file):
        with open(old_file, 'r') as open_old_file:
            logger.info('..tsv to csv')
            # run the csv script on the tsv files
            working_old_file = csv.reader(open_old_file,
                                          delimiter='\t')
            logger.debug('the current file being processed %s  ',
                         working_old_file)
            #creates in same folder
            with open(old_file[:-3] + 'csv', 'w') as new_file:
                wtr = csv.writer(new_file)
                for row in working_old_file:
                    if len(row) == 5:
                        wtr.writerow((row[1], row[2], row[4]))

    elif re.match('.*\.csv', old_file):

        logger.info('..csv to json')
        with open(old_file, 'r') as open_old_file:
            reader = csv.DictReader(f, fieldnames)
            # create count for rows to properly close json
            row_count = sum(1 for row in reader)
            # seek back to begining of file, so it can be read for writing
            open_old_file.seek(0)
            logger.info(row_count)
            logger.debug('the current file being processed %s  ', old_file)
            line_count = 0
            #creates in same folder
            with open(old_file + [:-3] + 'json', 'w') as new_file:
                new_file.write('[\n')
                for row in reader:
                    json.dump(row, new_file)
                    line_count += 1
                    if line_count != (row_count):
                        new_file.write(',\n')
                    else:
                        new_file.write('\n]')

    new_file.close()
    open_old_file.close()
    logger.debug('returning %s' new_file)
    return new_file


def __main__():
    #create logger
    logger = logging.getLogger(__name__)
    #logfile format
    formatter = logging.Formatter(
        "%(asctime)s %(name)s : %(levelname)s : \t %(message)s", "%d/%m/%Y %H:%M:%S")
    logger.setLevel(logging.DEBUG)

    #log level screen prints out to
    terminal_format = logging.Formatter("\n%(message)s")
    PR = logging.StreamHandler()
    PR.setLevel(logging.INFO)
    PR.setFormatter(terminal_format)
    logger.addHandler(PR)

    logger.debug('starting up...')

    #create parser options for cli
    parser = argparse.ArgumentParser(description=
    'foobar')
    parser.add_argument('-k', '--keys', help='Select the keys for your JSON file (ie the info to catch, POS is required)', default='.tsv')
    parser.add_argument('-o','--output', help='Select the file path for your output', required=False)
    parser.add_argument('-i','--input', help= 'Select the file path for your input(s)',required=False)
    parser.add_argument('-p','--path', help= 'Select the path of the files being working on, otherwise current directory is assumed',required=False)
    parser.add_argument('-t','--to_tag', help= 'The JSON object to run the tagger on, by defualt it is "Tweet"',required=False)
    #parser options for log file
    parser.add_argument("-v", "--verbose", help="show verbose logger", action="store_true")
    parser.add_argument("-l", "--log", help="log to file", action="store_true")

    arguments = parser.parse_args()

    #set the log levels
    if arguments.verbose:
        PR.setLevel(logging.DEBUG)
    elif arguments.log:
            #don't know if this naming convention will work
            logFilePath = str(_function.__name__)+".log"
            file_handler = logging.FileHandler(logFilePath)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
    while True:
        #applies if no args given that arent about logging
        if (len(sys.argv) == 1) or ((arguments.verbose or arguments.log) is not None):
            try:
                response_1 = input(
                    "\nPress Y to see a demo otherwise press N or Enter to exit\n")
                response_1 = response_1.lower()
                pass
            except ValueError:
                print ('Sorry, I did not understand that')
                continue
        y = ['y', 'yes', 'yeah']
        n = ['n', 'no', '']
        if response_1 in y:
            Demo_mode(_function)
            break
        elif response_1 in n:
            break
        #load function with input if everything goes smoothly
        else:
            load_tag(arguments.input, arguments.path, arguments.output, arguments.keys)


if __name__ == '__main__':
    __main__()
