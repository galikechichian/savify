# Author: Gali Kechichian
# Main script
from scraper import *
import streamlit as st

def space(): 
    st.write('\n\n')

st.title("Savify.")
st.subheader("Enjoy your favorite Spotify playlists offline.")

space()
space()

link = st.text_input("Paste public Spotify playlist URL:", "")

space()
space()

st.button('Download Playlist')

print(link)