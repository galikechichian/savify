# Author: Gali Kechichian
# Main script
from spotify import *
from youtube import *
import streamlit as st

def space(): 
    st.write('\n\n')

st.title("Savify.")
st.subheader("Enjoy your favorite Spotify playlists offline.")

space()

playlist_link = st.text_input(
    "Enter a valid Spotify playlist URL:", 
    placeholder="Paste URL here", 
    help="- Must be public\n- No more than 50 tracks",
    )

if playlist_link != "":
    response = ""
    with st.spinner("Loading your playlist..."):
        response = get_playlist(token, playlist_link)
        playlist_info = get_tracks(response)
    
    if (got_error(response)):
        st.error(playlist_info, icon="🚨")
    else:
        st.caption(f":green[_Playlist name:_] {playlist_info['playlist_name']}")
        playlist_size = len(playlist_info['tracks'])
        st.caption(f":green[_Number of tracks:_] {playlist_size}")
        if (playlist_size <= 50):
            st.button('Download Playlist')
        else:
            st.warning("Playlist is too big!", icon="⚠️")
