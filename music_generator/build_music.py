
import h5py
import tensorflow as tf
import joblib
from flask import send_file

def create_song():
  ###### REAL BEHAVIOR #######
  #bring the model
  #download_model.predict(song)
  #the song maybe from the user or directly saved in your gcp
  #save the song in new_song
  ################
  ###### DUMMY BEHAVIOR #######
  #load a song
  new_song = open('midi_songs_Eternal_Harvest.mid', 'rb')
  print(new_song)
  #return send_file(new_song, mimetype='audio/midi')
  return new_song

def download_model():
  MODEL_NAME = "music-generator-model"
  BUCKET_NAME = "music-generator-713"
  MODEL_VERSION = "0.1"
  LOCAL_MODEL_NAME = "model.h5"
  BUCKET_NAME = 'music-generator-713'
  BUCKET_TRAIN_DATA_PATH = 'data/'

  gcs_path = f"gs://{BUCKET_NAME}/models/{MODEL_NAME}/{MODEL_VERSION}/{LOCAL_MODEL_NAME}"
  print(gcs_path)
  loaded_model = tf.io.gfile.GFile(gcs_path, 'rb')
  model_gcs = h5py.File(loaded_model, 'r')
  print(model_gcs)
