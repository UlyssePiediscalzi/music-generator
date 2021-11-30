import ipdb
import streamlit as st
from music_generator import build_music
from os import path
from base64 import b64encode

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
    new_song = build_music.create_song()
    fpath = "raw_data/test_william.mid"
    st.markdown(get_binary_file_downloader_html(fpath, 'MIDI'), unsafe_allow_html=True)
