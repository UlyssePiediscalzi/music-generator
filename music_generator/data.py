import pypianoroll
import glob
import os
import math
from tensorflow.python.lib.io import file_io
import tensorflow as tf
from io import BytesIO


def get_npz_data(n, place):
    ''''
    Load n number of npz files from all of the folders contained in the raw_data folder
    '''
    # get a list of the possible filepaths for the npz files
    files = []

    if place == "colab":
      with open("/content/drive/MyDrive/lpd_5/list_file_drive.txt", 'r') as f:
        for line in f:
          files.append(line.rstrip('\n'))
    elif place == "gcp":
      with open("list_file_gcp_test.txt", 'r') as f:
        for line in f:
          files.append(line.rstrip('\n'))
    else:
      with open("../list_file_local.txt", 'r') as f:
        for line in f:
          files.append(line.rstrip('\n'))

    # Load n files from the dataset

    if place == "gcp":
      BUCKET_NAME = 'music-generator-713'
      BUCKET_TRAIN_DATA_PATH = 'data/'

      multitracks = []
      for file in files:
        f = BytesIO(file_io.read_file_to_string(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}{file}", binary_mode=True))
        multitracks.append(pypianoroll.load(f))
    else:
      multitracks = [pypianoroll.load(fp) for fp in files[0:n]]

    return multitracks


def multitrack_to_midi(multitracks, save_path='raw_data/midi'):
    '''
    Given a list of multitrack objects convert each of them into a midi file
    and save it on the raw_data folder
    '''
    for i in range(len(multitracks)):
        pypianoroll.write(f'{save_path}/track{i}.midi', multitracks[i])
    return 'midi files saved successfully'


def fetching_instrument_pianorolls(multitracks, instrument):
    '''Takes the output of get_npz_data() function and a
    string corresponding either to : Piano, Bass, Drum, Strings, Guitar.
    Returns a list of arrays'''
    pianoroll_arrays = []
    for multi in multitracks:
        for standard in multi:
            if standard.name in instrument and standard.pianoroll.shape[0] != 0:
                pianoroll_arrays.append(standard.pianoroll)
    return pianoroll_arrays

def average_non_zeros(sample):
    average_array = []
    for row in sample:
      mean = row[np.nonzero(row)].mean()
      if math.isnan(mean):
        average_array.append(0)
      else:
        average_array.append(mean)

    return np.array(average_array)
