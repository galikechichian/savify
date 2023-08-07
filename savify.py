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
    "Enter a valid Spotify playlist URL:", 
    placeholder="Paste URL here", 
    help="Note: your playlist needs to be public",
    )

if playlist_link != "":
    response = ""
    with st.spinner("Loading your playlist..."):
        response = get_playlist(token, playlist_link)
        playlist_info = get_tracks(response)
    
    if (got_error(response)):
        st.error(playlist_info, icon="🚨")
    else:
        st.caption(f"_Playlist name:_ {playlist_info['playlist_name']}")
        st.caption(f"_Number of tracks:_ {len(playlist_info['tracks'])}")
        st.button('Download Playlist')