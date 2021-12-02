import streamlit as st
from music_generator import build_music
from os import path
from base64 import b64encode
from random import randrange
import requests
import json
from music21 import stream, note
import pretty_midi
from scipy.io import wavfile
import numpy as np
import io

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{path.basename(bin_file)}">Download {file_label}</a>'
    return href

st.set_page_config(
    page_title="Piano Melodies Generator 1.0",  # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

st.title('Piano Melodies Generator 1.0')

# if st.checkbox("Run", key="A"):
if st.button("Generate new notes"):
    url = "https://music-generator-api-zyjtckkcoa-uc.a.run.app/random_notes"
    local_url = "http://localhost:8000/random_notes"

    with st.spinner('Wait for it...'):
      response = requests.get(url)
      response = response.json()
      st.success('Notes created!')

    st.session_state.user_input_notes = json.loads(response["user_input_notes"])
    st.session_state.user_input_durations = json.loads(response["user_input_durations"])
    basic_melody = build_music.chords_n_notes(st.session_state.user_input_notes, st.session_state.user_input_durations)
    basic_melody_midi = stream.Stream(basic_melody)
    three_notes_sounds = f"random_notes_{randrange(1000)}"
    fpath = f"{three_notes_sounds}.mid"
    midi_file = basic_melody_midi.write('midi', fp=fpath)

    with st.spinner(f"Transcribing to FluidSynth"):
      midi_data = pretty_midi.PrettyMIDI(midi_file)
      audio_data = midi_data.synthesize()
      audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
      )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

      virtualfile_basic = io.BytesIO()
      wavfile.write(virtualfile_basic, 44100, audio_data)

    col1, col2, col3 = st.columns(3)
    col1.metric("First Note", st.session_state.user_input_notes[0])
    col2.metric("Second Note", st.session_state.user_input_notes[1])
    col3.metric("Third Note", st.session_state.user_input_notes[2])

    st.audio(virtualfile_basic)


# if st.checkbox("Run", key="B"):
def update_first():
    st.session_state.second = st.session_state.first

if st.button('Create new song'):
    url = "https://music-generator-api-zyjtckkcoa-uc.a.run.app/predict"
    local_url = "http://localhost:8000/predict"


    with st.spinner('Wait for it...'):

      params = {
          "user_input_notes": json.dumps(st.session_state.user_input_notes),
          "user_input_durations": json.dumps(st.session_state.user_input_durations)
      }
      response = requests.get(url, params = params)
      response = response.json()
      Music_notes = response['notes']
      Music_notes = json.loads(Music_notes)

      Music_durations = response['durations']
      Music_durations = json.loads(Music_durations)

      col1, col2, col3 = st.columns(3)
      col1.metric("First Note", st.session_state.user_input_notes[0])
      col2.metric("Second Note", st.session_state.user_input_notes[1])
      col3.metric("Third Note", st.session_state.user_input_notes[2])

      # CREATE MELODY
      Melody = build_music.chords_n_notes(Music_notes, Music_durations)
      # build_music.show(Melody)
      Melody_midi = stream.Stream(Melody)
      song_name = f"test_song_number_{randrange(1000)}"
      fpath = f"{song_name}.mid"
      midi_file = Melody_midi.write('midi', fp=fpath)

      with st.spinner(f"Transcribing to FluidSynth"):
        midi_data = pretty_midi.PrettyMIDI(midi_file)
        audio_data = midi_data.synthesize()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)

        st.success('Listen the next hit!')
    st.audio(virtualfile)
    col7, col8, col9 = st.columns(3)
    #col2.markdown(get_binary_file_downloader_html(fpath, 'MIDI'), unsafe_allow_html=True)
    st.download_button(
        label="Download midi file",
        data=fpath,
        file_name=fpath,
        mime='audio/mid',
    )


