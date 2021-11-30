
#import random
#import tensorflow as tf
#rom tensorflow import keras
#from tensorflow.keras.models import load_model
#import h5py
#import music21
#import glob
import numpy as np
#import os
from music21 import converter, instrument, note, chord, stream, tempo, duration
import matplotlib.pyplot as plt
#import pickle
#from tensorflow.keras.utils import to_categorical
#from tensorflow.keras import layers, models
# from music_generator.midi import parseNote, get_notes, render_midi
#from tensorflow.keras.optimizers import RMSprop
#from tensorflow.keras.models import load_model

#model = load_model("raw_data/model_40seq_196voc_5tracks.h5")

# def create_song(song_name):
#   ###### REAL BEHAVIOR ######

#   Music_notes, Melody = Malody_Generator(200)
#   #the song maybe from the user or directly saved in your gcp
#   #save the song in new_song
#   ################
#   ###### DUMMY BEHAVIOR #######
#   #load a song
#   Melody.write('midi', fp=f'raw_data/{song_name}.mid')
#   #new_song = open('raw_data/test_william.mid', 'rb')
#   #print(new_song)
#   #return send_file(new_song, mimetype='audio/midi')
#   return Melody

# def download_model():
#   MODEL_NAME = "music-generator-model"
#   BUCKET_NAME = "music-generator-713"
#   MODEL_VERSION = "0.1"
#   LOCAL_MODEL_NAME = "model.h5"
#   BUCKET_NAME = 'music-generator-713'
#   BUCKET_TRAIN_DATA_PATH = 'data/'

#   gcs_path = f"gs://{BUCKET_NAME}/models/{MODEL_NAME}/{MODEL_VERSION}/{LOCAL_MODEL_NAME}"
#   print(gcs_path)
#   loaded_model = tf.io.gfile.GFile(gcs_path, 'rb')
#   model_gcs = h5py.File(loaded_model, 'r')
#   print(model_gcs)


def chords_n_notes(Snippet):
  Melody = []
  offset = 0  # Incremental
  for i in Snippet:
      #If it is chord
      if ("." in i or i.isdigit()):
          chord_notes = i.split(".")  # Seperating the notes in chord
          notes = []
          for j in chord_notes:
              inst_note = int(j)
              note_snip = note.Note(inst_note)
              notes.append(note_snip)
              chord_snip = chord.Chord(notes)
              chord_snip.offset = offset
              Melody.append(chord_snip)
      # pattern is a note
      else:
          note_snip = note.Note(i)
          note_snip.offset = offset
          Melody.append(note_snip)
      # increase offset each iteration so that notes do not stack
      offset += 0.5
  Melody_midi = stream.Stream(Melody)
  return Melody_midi

# def Malody_Generator(Note_Count):
#     pickle_model = pickle.load(open('raw_data/wil_deploy_dummy.pickle', 'rb'))
#     network_input = pickle_model['network_input']
#     print(len(network_input))
#     pitchnames = pickle_model['pitchnames']

#     seed = network_input[np.random.randint(0, len(network_input)-1)]
#     Music = ""
#     Notes_Generated = []
#     int_to_note = dict((number, note)
#                        for number, note in enumerate(pitchnames))
#     for i in range(Note_Count):
#         n_vocab = len(int_to_note)
#         seed = seed.reshape(1, 40, 1)
#         prediction = model.predict(seed, verbose=0)[0]
#         prediction = np.log(prediction)  # diversity
#         exp_preds = np.exp(prediction) / 1
#         prediction = exp_preds / np.sum(exp_preds)
#         index = np.argmax(prediction)
#         index_N = index / float(n_vocab)
#         Notes_Generated.append(index)
#         Music = [int_to_note[char] for char in Notes_Generated]
#         seed = np.insert(seed[0], len(seed[0]), index_N)
#         seed = seed[1:]
#     #Now, we have music in form or a list of chords and notes and we want to be a midi file.
#     Melody = chords_n_notes(Music)
#     Melody_midi = stream.Stream(Melody)
#     return Music, Melody_midi
