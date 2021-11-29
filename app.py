import streamlit as st
from music_generator import build_music
from os import path
from base64 import b64encode

st.write('MUSIC-GENERATOR')

###############################
def get_binary_file_downloader_html(bin_file, file_label='File'):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
    except FileNotFoundError as e:
        exit_on_exception(e, 'open() in ' +
                          'get_binary_file_downloader_html()')

    bin_str = b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{path.basename(bin_file)}">Download {file_label}</a>'
    return href
#################################


all_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#',
             'G', 'G#']
first_note = st.selectbox('Select first note', all_notes)
second_note = st.selectbox('Select second note', all_notes)
third_note = st.selectbox('Select third note', all_notes)
st.write(f"{first_note} {second_note} {third_note}")

########SEND_NOTES################
if st.button('Send notes for predict'):
    # print is visible in the server output, not in the page
    st.write('I was clicked 🎉')

else:
    st.write('I was not clicked 😞')

########RECEIVE_NEW_MIDI################

if st.button('request midi file'):
    # print is visible in the server output, not in the page
    new_song = build_music.create_song()
    st.write('I was clicked 🎉')
    st.write(new_song)

    audio_bytes = new_song.read()
    st.audio(audio_bytes, format='mid')
    fpath = "midi_songs_Eternal_Harvest.mid"
    st.markdown(get_binary_file_downloader_html(fpath, 'MIDI'), unsafe_allow_html = True)
else:
    st.write('I was not clicked 😞')
