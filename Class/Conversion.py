import datetime as dt
import hashlib
import json
import os
import shutil
from collections import defaultdict
from typing import Union
import chardet

"""
This class is a storage locker for function I use to convert files, check file info
    
"""


# ToDo: Create Unit Testing for class fucntions

class Utility:

    # noinspection PyUnboundLocalVariable
    @classmethod
    def naming(cls, descriptor: str, lang: str, length: int, ext: str, long_date: bool = True) -> str:
        """
        function to name files given a few features
        :param descriptor: short descriptor of the file use-case like `black_cat_hats`
        :param lang: 4 char language code like `en_us`
        :param length: length of output, if not given will not show
        :param ext: extension to go with name
        :param long_date: bool to denote if filename should include just date, or date time, defaults to just date
        :return new_name: name converted from input
        """
        # Naming convention based on vars given
        if lang is None:
            new_name = f'{descriptor}-{length}-{cls.now(long_time=long_date)}.{ext}'
        elif lang is None and length is None:
            new_name = f'{descriptor}-{cls.now(long_time=long_date)}.{ext}'
        elif descriptor is None:
            new_name = f'Data-{lang}-{length}-{cls.now(long_time=long_date)}.{ext}'
        elif descriptor is None and lang is None:
            new_name = f'Data-{length}-{cls.now(long_time=long_date)}.{ext}'
        elif descriptor is None and length is None:
            new_name = f'Data-{lang}-{cls.now(long_time=long_date)}.{ext}'
        elif length is None:
            new_name = f'{descriptor}-{lang}-{cls.now(long_time=long_date)}.{ext}'
        else:
            new_name = f'{descriptor}-{lang}-{length}-{cls.now(long_time=long_date)}.{ext}'

        return new_name

    @staticmethod
    def group_data(in_array: list, var: str, group_size: int = 3) -> tuple[
        Union[dict[list], dict], Union[dict[list], dict]]:
        """
        Function to group unites based on dict key variable
        and return all, and those in groupings of specified group size
        :param in_array: an array of dict objects
        :param group_size: minimum size needed to return groupings
        :param var: variable to use as keyword to be searched in dict keys
        :return: out - group with size info, groups - all items
        """
        groups = defaultdict(list)
        out = defaultdict(list)

        for i in in_array:
            groups[i[var]].append(i)

        for k, v in dict(groups).items():
            if len(v) >= group_size:
                out[k] = v
                continue

        print(f'Total unique items: {len(in_array)}')
        print(f'Total unique groupings: {len(groups)}')
        print(f'Total unique groupings of {group_size}  or more: {len(out)}')
        return dict(out), dict(groups)

    @classmethod
    def cycle_through(cls, location: str = "./", new_location: str = "./", known_unique: dict = None,
                      folder_names: dict = None, ignore: dict = None):
        """
        Script to copy data from a multitude of folders to new single location, with only unique items
        :param location: Location of the input data to run the script over
        :param new_location: Location to copy the data to
        :param known_unique: complete dict of already known items
        :param folder_names: conversions of the folder-names to the datasets
        :param ignore: array of files to ignore
        :return: updated unique_id list
        """
        known_unique = known_unique if known_unique else {}
        folder_names = folder_names if folder_names else {}
        ignore = ignore if ignore else {}

        for root, dirs, files in os.walk(location):
            for c, i in enumerate(files):

                if i == "" or i in ignore:
                    continue
                # create dict for item if it doesn't already exist
                if i not in list(known_unique.keys()):
                    known_unique[i] = {}
                # Check if the item associated with the user is in the collection already
                try:
                    if i in list(known_unique[i].keys()):
                        continue
                except TypeError:
                    pass

                cls.copy_organize(i, root, new_location, folder_names)
                location_in_list = root.split("\\")[-3:]
                country = [folder_names[location_in_list[0]]]
                file_location = country + location_in_list[1:]
                known_unique[i].update({i: file_location})

        return known_unique

    @staticmethod
    def copy_organize(file_name: str, old_path: str, new_path: str, titles: dict):
        """
        Copy data from original location to new location, to organize data
        :param file_name: file to copy
        :param old_path: location from which to pull the data
        :param new_path: location to push the data to
        :param titles: dict of folder-names
        :return: copied file
        """
        old_loc = os.path.join(old_path, file_name)
        pathing = old_path.split("\\")[-3:]
        group = pathing[0]
        new_group = titles[group]
        new_loc = os.path.join(new_path, new_group, *pathing[1:])

        try:
            os.makedirs(new_loc)
        except FileExistsError:
            # directory already exists
            pass
        try:
            shutil.copy2(old_loc, os.path.join(new_loc, file_name))
        except shutil.SameFileError:
            pass
        except OSError:
            with open("issues.txt", "a") as f:
                f.write(f"\n{old_loc}\t{new_loc}\t{file_name}")

    @staticmethod
    def get_md5_hash(filepath: str, chunk_size: int = 8192) -> hashlib.md5:
        """
        Get the MD5 hash for a file, useful to verify file, or if you want to create a unique name for your file
        :param filepath: Path to file to build hash of
        :param chunk_size: bytes of the file to load at a time
        :return: md5 hash of the file
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)

        with open(filepath, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(chunk_size)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(chunk_size)
        return file_hash

    @staticmethod
    def predict_file_encoding(filepath: str, sample_size: int = 200) -> dict:
        """
        Uses Chardet module to identify the encoding of a file.
            Will read up to the sample_size lines in the file to make the prediction
        :param filepath: Path to file
        :param sample_size: Number of lines of a file to read.
            Prevents needing to load full file into memory when working with large files.
        :return:dictionary with the predicted encoding and confidence in prediction
            {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
        """
        assert os.path.exists(filepath)
        test_str = b""
        count = 0
        with open(filepath, "rb") as x:
            line = x.readline()
            while line and count < sample_size:
                test_str += line
                count = count + 1
                line = x.readline()

        return chardet.detect(test_str)

    @staticmethod
    def show(ingested: Union[list, dict], size: int = 2):
        """
        Used to show a few lines as example output
            Assumes normal dictionaries
        :param ingested: a list or dict to be previewed
        :param size: how many lines to view
        :return: print to display a few lines
        """

        if type(ingested) is dict:
            for c, (k, v) in enumerate(ingested.items(), 0):
                try:
                    # will show in Jupyter
                    display(k, v, '--------')
                except (KeyError, NameError):
                    print(k, v, '--------')
                if c == size:
                    break
        elif type(ingested) is defaultdict:
            for c, (k, v) in enumerate(ingested.items(), 0):
                try:
                    # Will show in Jupyter
                    display(k, dict(v), '--------')
                except (KeyError, NameError):
                    print(k, dict(v))
                if c == size:
                    break
        elif type(ingested) is list:
            for c, (i) in enumerate(ingested, 0):
                try:
                    # Will show in Jupyter
                    display(i, '--------')
                except KeyError:
                    print(i, '--------')
                if c == size:
                    break

    # noinspection PyUnboundLocalVariable
    @staticmethod
    def now(long_time: bool = False) -> str:
        """
        Function to add the date in yyyy_mm_dd (hh_mm_ss)
        :param long_time: flag to show hour, minute and second info, off by default
        :return string_time: date as string
        """

        current_time = dt.datetime.now() + dt.timedelta(seconds=0)
        if not long_time:
            string_time = current_time.strftime('%Y_%m_%d.%H_%M_%S')
        elif long_time is True:
            string_time = current_time.strftime('%Y_%m_%d')
        return str(string_time)

    @staticmethod
    def check_file(filepath: str) -> str:
        """
        Check file to see if is greater than 0 bytes
        :return: 'fine' or 'problem' depending on if it is a non-empty file
        """
        file_bytes = os.stat(filepath).st_size
        if file_bytes == 0:
            return 'problem'
        return 'fine'

    @classmethod
    def check_for_empty(cls, filepath: str, bad_files: dict = None):
        """
        Function to walk through files and check if the data is 0 bytes or not
        :param filepath: directory to review
        :param bad_files: a dict of files which are empty
        :return: returns a dict of files which are empty or None, if applicable
        """
        bad_files = bad_files if bad_files else {}
        bad_babies = 0
        for root, dirs, files in os.walk(filepath):
            for ff in files:
                temp_file = os.path.join(root, ff)
                if cls.check_file(temp_file) == 'problem':
                    bad_files[ff] = root
                    bad_babies += 1
        print(f'{bad_babies} bad files found')
        if len(bad_files) > 0:
            return bad_files
        else:
            return None

    @staticmethod
    def check_json(singlet: str) -> Union[dict, str]:
        """
        used to check if a string input is really a json/dict in string form
        :param singlet: line of string, that may or may not be a json/dict item
        :return: converted string or just string if not a json/dict
        """
        try:
            out = json.loads(singlet)
        except (TypeError, json.JSONDecodeError):
            out = singlet

        return out
