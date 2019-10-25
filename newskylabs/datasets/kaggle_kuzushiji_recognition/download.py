"""newskylabs/datasets/kaggle_kuzushiji_recognition/download.py:

See:

  - Kuzushiji Recognition
    Opening the door to a thousand years of Japanese culture
    https://www.kaggle.com/c/kuzushiji-recognition/

"""

__author__      = "Dietrich Bollmann"
__email__       = "dietrich@formgames.org"
__copyright__   = "Copyright 2019 Dietrich Bollmann"
__license__     = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__        = "2018/02/25"

import os
from pathlib import Path

import numpy as np

from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.api_client import ApiClient

from newskylabs.collagen.utils.settings import get_setting
from newskylabs.collagen.utils.collagen import get_data_dir

## =========================================================
## Kuzushiji Recognition Dataset Settings
## ---------------------------------------------------------

_dataset_settings = {
    'name': 'kaggle-kuzushiji-recognition',
    'archive': {
        'name': 'kuzushiji-recognition.zip',
        'content': {
            'translation':         'unicode_translation.csv',
            'sample-submission':   'sample_submission.csv',
            'train-csv':           'train.csv',
            'test-images':         'test_images.zip',
            'train-images':        'train_images.zip',
        },
    },
    'kanji-font': {
        'url': 'https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip',
        'name': 'NotoSansCJKjp-hinted.zip',
        'content': {
            'otf': 'NotoSansCJKjp-Regular.otf',
        },
    },
}

## =========================================================
## Listing the Kuzushiji Recognition Competition Dataset files
## ---------------------------------------------------------
## 
## Command:
## 
## kaggle competitions files -c kuzushiji-recognition
## 
## Output:
## 
## > name                      size  creationDate
## > -----------------------  -----  -------------------  
## > unicode_translation.csv   51KB  2019-07-25 14:32:40  
## > sample_submission.csv    146KB  2019-07-25 14:32:47  
## > train.csv                 15MB  2019-07-25 14:32:48  
## > test_images.zip            4GB  2019-07-25 14:32:48  
## > train_images.zip           3GB  2019-07-25 14:32:48  
## 
## api.competition_list_files_cli() is implemented in: 
##   site-packages/kaggle/api/kaggle_api_extended.py
## 
## And used in: 
##   site-packages/kaggle/cli.py
## 
## ==========================================================
## My own version:
## ----------------------------------------------------------

def kuzushiji_recognition_list_files():
    """List files of kuzushiji-recognition competition.

    See:
    Kuzushiji Recognition
    Opening the door to a thousand years of Japanese culture
    https://www.kaggle.com/c/kuzushiji-recognition/
    """
    
    # Authenticate
    api = KaggleApi(ApiClient())
    api.authenticate()

    # Get competition from config
    competition = None

    # Competition option normally provided by cli
    competition_opt = "kuzushiji-recognition"

    # Print as Table, not as comma separated values
    csv_display = False

    # Suppress verbose output (default)
    quiet = False

    # Use the cli wrapper to list the files
    # 
    # Parameters:
    # - competition: the name of the competition. If None, look to config
    # - competition_opt: an alternative competition option provided by cli
    # - csv_display: if True, print comma separated values
    # - quiet: suppress verbose output (default is False)
    # 
    api.competition_list_files_cli(competition,
                                   competition_opt=competition_opt,
                                   csv_display=csv_display,
                                   quiet=quiet)

# TEST
#| kuzushiji_recognition_list_files()

## =========================================================
## Downloading the Kuzushiji Recognition Competition Dataset
## ---------------------------------------------------------
## 
## Command:
## 
## kaggle competitions download -c kuzushiji-recognition
## 
## api.competition_download_cli() is implemented in: 
##   site-packages/kaggle/api/kaggle_api_extended.py
## 
## And used in: 
##   site-packages/kaggle/cli.py
## 
## ---------------------------------------------------------

def kuzushiji_recognition_download_dataset(path='/tmp/kuzushiji'):
    """Download the dataset of kuzushiji-recognition competition.

    See:
    Kuzushiji Recognition
    Opening the door to a thousand years of Japanese culture
    https://www.kaggle.com/c/kuzushiji-recognition/

    Parameters
    =========
    PATH: a path to download the file to
    """
    
    # Authenticate
    api = KaggleApi(ApiClient())
    api.authenticate()

    # The name of the competition
    competition = None

    # An alternative competition option provided by cli
    competition_opt = "kuzushiji-recognition"

    # The configuration file name
    file_name = None

    # Force the download if the file already exists (default False)
    force = False

    # Suppress verbose output (default)
    quiet = False

    # Use the cli wrapper to download the files
    # 
    # Parameters:
    # - competition: the name of the competition
    # - competition_opt: an alternative competition option provided by cli
    # - file_name: the configuration file name
    # - path: a path to download the file to
    # - force: force the download if the file already exists (default False)
    # - quiet: suppress verbose output (default is False)
    api.competition_download_cli(competition=competition,
                                 competition_opt=competition_opt,
                                 file_name=file_name,
                                 path=path,
                                 force=force,
                                 quiet=quiet)

# TEST
#| path = '/tmp/kuzushiji'
#| kuzushiji_recognition_download_dataset(path)

## =========================================================
## Dataset directory
## ---------------------------------------------------------

def get_create_data_dir():
    """Get the data directory.
    When the directory does not exist it is created.
    """

    # Calculate the dataset data dir
    data_dir = Path(get_data_dir()).expanduser()
    dataset = _dataset_settings['name']
    dataset_dir = data_dir / dataset

    # Ensure that the directlry exists
    dataset_dir.mkdir(parents=True, exist_ok=True)

    return dataset_dir

## =========================================================
## 'kaggle-kuzushiji-recognition' dataset
## ---------------------------------------------------------

def download_dataset():
    """Download and upack the dataset."""

    # Ensure that the directlry exists
    dataset = _dataset_settings['name']
    dataset_dir = get_create_data_dir()

    # Get the name
    archive = _dataset_settings['archive']['name']
    archive_path = dataset_dir / archive
    
    # Print a header 
    print("Downloading the dataset {}".format(dataset))
    print("containing the following files:\n")
    kuzushiji_recognition_list_files()
    print("")

    # Download the dataset
    kuzushiji_recognition_download_dataset(dataset_dir)

    # Unzip the archive
    import zipfile
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)

    # Remove the archive
    archive_path.unlink()
    
def get_dataset_file_path(name):
    """Get the file path for dataset file referred to by NAME.
    """
    
    # Ensure that NAME is not the dataset archive
    # This function only works for the files / directories 
    # contained in the archive
    if name == 'name':

        # Unknown dataset file
        print("ERROR {} is the dataset archive.".format(_dataset_settings['archive'][name]))
        print("")
        print("To list the content of the archive use:")
        print("kaggle competitions files -c kuzushiji-recognition")
        print("")
        print("To download the archive via the command line use:")
        print("kaggle competitions download -c kuzushiji-recognition")
        print("")
        exit(-1)

    # Ensure that NAME refers to a known dataset file
    if not name in _dataset_settings['archive']['content'].keys():

        # Unknown dataset file
        print("ERROR Unknown dataset file: {}".format(name))
        exit(-1)

    # Ensure that the file has been downloaded
    filepath = get_create_data_dir() / _dataset_settings['archive']['content'][name]

    # Ensure that the file exists
    if not filepath.exists():
        download_dataset()

    return filepath
        
## =========================================================
## Kanji Font (NotoSansCJKjp-Regular.otf)
## ---------------------------------------------------------

def download_kanji_font_otf_file():
    """Download the japanese font NotoSansCJKjp-hinted.zip."""

    # Get the kanji font information
    url = _dataset_settings['kanji-font']['url']
    archive_filename = _dataset_settings['kanji-font']['name']
    otf_filename = _dataset_settings['kanji-font']['content']['otf']

    data_dir = get_create_data_dir()
    archive_path = data_dir / archive_filename
    otf_file_path = data_dir / otf_filename

    # Download the font archive
    import urllib
    print("Downloading the font archive {}".format(url))
    urllib.request.urlretrieve(url, archive_path)

    # Extract the font otf file
    import zipfile
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # zip_ref.extractall(data_dir)
        zip_ref.extract(otf_filename, data_dir)

    # Remove the archive
    archive_path.unlink()

    # Return the path of the font otf file
    return otf_file_path

def get_kanji_font_file_path():
    """Get the path of the kanji font used to label the dataset.
    When the font has not been downloaded yet download it.
    """
    
    # Ensure that the file has been downloaded
    data_dir = get_create_data_dir()
    otf_filename = _dataset_settings['kanji-font']['content']['otf']
    filepath = data_dir / otf_filename

    # Ensure that the file exists
    if not filepath.exists():
        download_kanji_font_otf_file()

    return filepath

## =========================================================
## TEST
## ---------------------------------------------------------

def test():
    """
    Test the download functions.
    """

    name = 'translation'
    #| name = 'sample-submission'
    #| name = 'train-csv'
    #| name = 'test-images'
    #| name = 'train-images'
    filepath = get_dataset_file_path(name)
    print("DEBUG filepath:", filepath)
    
    kanji_font_filepath = get_kanji_font_file_path()
    print("DEBUG kanji font filepath:", kanji_font_filepath)

## =========================================================
## =========================================================

## fin.
