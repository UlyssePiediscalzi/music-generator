import streamlit as st
from music_generator import build_music
from os import path
from base64 import b64encode

st.title('Music-Generator 1.0: Music Generation with an LSTM Neural Network')

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


col1, col2, col3 = st.columns(3)
all_notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#',
             'G', 'G#']

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
st.subheader(f"{first_note} {second_note} {third_note}")


########SEND_NOTES################
if st.button('CREATE NEW SONG'):
    #CALL BUILD_MUSIC/CREATE:SONG
    new_song = build_music.create_song(notes)

    #TRYING PLAYING DIRECTLY IN THE PAGE
    st.write(new_song)
    audio_bytes = new_song.read()
    st.audio(audio_bytes, format='mid')

    #TODO-CHANGE-PATH
    fpath = "midi_songs_Eternal_Harvest.mid"
    st.markdown(get_binary_file_downloader_html(fpath, 'MIDI'), unsafe_allow_html=True)

else:
    st.write('I was not clicked 😞')
