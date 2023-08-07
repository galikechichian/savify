# Author: Gali Kechichian
# Main script
from scraper import *
import streamlit as st

def space(): 
    st.write('\n\n')

st.title("Savify.")
st.subheader("Enjoy your favorite Spotify playlists offline.")

space()

playlist_link = st.text_input(
    "Enter your Spotify playlist URL:", 
    placeholder="Paste URL here", 
    help="Note: your playlist needs to be public",
    )

if playlist_link != "":
    response = ""
    with st.spinner("Loading your playlist..."):
        response = get_playlist(token, playlist_link)
        print(response)
    
    if (got_error(response)):
        st.error(get_tracks(response), icon="🚨")

space()
space()

# st.button('Download Playlist')

print(playlist_link)