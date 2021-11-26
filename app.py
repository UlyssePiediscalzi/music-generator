import numpy as np
from music_generator.data import get_npz_data
import streamlit as st


st.markdown("""# This is a header
## This is a sub header
This is text""")


st.write(get_npz_data(10, "gcp"))
