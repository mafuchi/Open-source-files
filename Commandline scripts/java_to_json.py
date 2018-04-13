#!/usr/bin/env python3

import json, subprocess, codecs, os, shutil

_author__ = "Michael Madden"
__copyright__ = "Copyright 2017, Michael Madden"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "mmadden.linguist@gmail.com"
__status__ = "Development"

def load_tag(infile, outfile):
    data_file=[]
    with open(infile, 'r') as json_data, open(outfile, 'w') as f:
        if not os.path.exists('./temp/'):
            os.mkdir('./temp/')
        json_file = json.load(json_data)
        json_data.close()
        f.write('[\n')
        #create a list to be used in conjugction with the
        # labels list to create dictionaires for tagging tweet
        #to be used for the tagged tweet
        keys = ['Word_order', 'Word', 'POS', 'Probability']

        for i in json_file:

            #to set the order of the the tagged item
            j = 0

            temp_file = open('./temp/temp_file.txt', 'w')

            #takes the tweet in the JSON object
            #(i["key_word"]) for a specific dict
            temp =  (i[u"Tweet"])
            temp_file.write((temp))
            temp_file.close()

            #option output to show sentences being parsed
            with codecs.open('./temp/temp_file.txt', "r",encoding='utf-8', errors='ignore') as fdata:
                for p in fdata:
                    print (str(p))
            fdata.close()

            #take the java program and have it run
            #line by line tweets
            with open('./temp/temp_file2.txt', 'w') as g:
                subprocess.call(['java', '-jar', '../ark-tweet-nlp-0.3.2.jar',
                                 '--output-format', 'conll', './temp/temp_file.txt'],
                stdout=g)
            g.close()

            #open the created temp file to check it is saving the parsed tweet
            with open('./temp/temp_file2.txt', 'r') as sdata:
                Dicts =[]
                #create a dictionary from the output
                for q in sdata:
                    values = []
                    j += 1 #for word order
                    values.append(j)
                    q = q.rstrip()
                    values = values + (q.split('\t'))
                    dictionairy = dict(zip(keys, values))
                    Dicts.append(dictionairy)
                    i.update({'Tagged' : Dicts }) #append dictionaries to tweet
                    tweetPOS=[] #collect all the POS for each tweet and make a new entry
                    for word in i['Tagged']:
                        #incase there is a null obj attached
                        try:
                            tweetPOS.append(word['POS'])
                        except:
                            pass

                    #after the while statement has finished join the POS of the sentence
                    h = ' '.join(tweetPOS)

                    #add the new POS to the list of sentences
                    i.update({'POS_S':h})

                sdata.close()

            #create an output file
            data_file.append(i)
        json.dump(data_file, f, indent=1)
        #add the end brackets to the file to be valid JSON.
        f.write('\n]')
    #remove temp files
    shutil.rmtree('./temp/')
    f.close()
    print ('temp files removed\n')

def __main__():

    arg_ = "../data/JSON/Set_1_tweet.SARCASM.all.id.DEV_full.json"
    arg_out ="../data/JSON/Set_1_tweet.SARCASM.all.id.DEV_full_Tagged.json"
    load_tag(arg_,arg_out)

if __name__ == '__main__':
    __main__()
