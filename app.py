import streamlit as st
from music_generator import build_music
from os import path
from base64 import b64encode
from random import randrange
import requests
import json
from music21 import stream
import pretty_midi
from scipy.io import wavfile
import numpy as np
import io

st.set_page_config(
    page_title="Music-Generator 1.0",  # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

st.title('Music-Generator 1.0: Music Generation with an LSTM Neural Network')

###############################

def get_binary_file_downloader_html(bin_file, file_label='File'):
    #ipdb.set_trace()

    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{path.basename(bin_file)}">Download {file_label}</a>'
    return href
#################################

col1, col2, col3 = st.columns(3)
all_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

with col1:
  st.subheader("Select 1st Note")
  first_note = st.selectbox('Select first note', all_notes)

with col2:
  st.subheader("Select 2nd Note")
  second_note = st.selectbox('Select second note', all_notes)

with col3:
  st.subheader("Select 3rd Note")
  third_note = st.selectbox('Select third note', all_notes)

notes = [first_note, second_note, third_note]

st.header("Notes:")
st.subheader(f"{first_note} {second_note} {third_note}  .")

if st.button('CREATE NEW SONG'):
    url = "https://music-generator-api-zyjtckkcoa-uc.a.run.app/predict"
    local_url = "http://localhost:8000/predict"
    #CALL API
    response = requests.get(url)
    response = response.json()
    Music_notes = response['notes']
    Music_notes = json.loads(Music_notes)

    #FINISHING CALLING API

    # CREATE MELODY
    Melody = build_music.chords_n_notes(Music_notes)
    Melody_midi = stream.Stream(Melody)
    song_name = f"test_song_number_{randrange(1000)}"
    fpath = f"{song_name}.mid"
    midi_file = Melody_midi.write('midi', fp=fpath)
    st.markdown(get_binary_file_downloader_html(fpath, 'MIDI'), unsafe_allow_html=True)

    with st.spinner(f"Transcribing to FluidSynth"):
      midi_data = pretty_midi.PrettyMIDI(midi_file)
      audio_data = midi_data.fluidsynth()
      audio_data = np.int16(
          audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
      )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

      virtualfile = io.BytesIO()
      wavfile.write(virtualfile, 44100, audio_data)

    st.audio(virtualfile)

else:
    st.write('I was not clicked 😞')


