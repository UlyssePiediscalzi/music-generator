import ipdb
from tensorflow.python.lib.io import file_io
import tensorflow as tf
from io import BytesIO
import pypianoroll
import numpy as np
from music_generator.data import get_npz_data

### GCP configuration - - - - - - - - - - - - - - - - - - -

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'music-generator-713'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

BUCKET_TRAIN_DATA_PATH = 'data/'

##### Training  - - - - - - - - - - - - - - - - - - - - - -

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
#MODEL_NAME = 'taxifare'

#multi = pypianoroll.load("gs://music-generator-713/data/lpd_5/lpd_5_cleansed/R/R/A/TRRRAJP128E0793859/2c78d25cb52eb48f767186ddaf11b191.npz")
#     multitrack = pypianoroll.load(f)

#print(multi)

# client = storage.Client()
# bucket = client.bucket(BUCKET_NAME)

# blobs = list(bucket.list_blobs(prefix='data/'))

# read_output = blobs[10].download_as_string()
# pypianoroll.load(blobs[10])

# print(read_output)



ipdb.set_trace()
