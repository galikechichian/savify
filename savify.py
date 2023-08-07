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
    help="- Must be public\n- No more than 30 tracks",
    )


if playlist_link != "":
    response = ""
    with st.spinner("Loading your playlist..."):
        response = get_playlist(token, playlist_link)
        playlist_info = get_tracks(response)
    
    if (got_error(response)):
        st.error(playlist_info, icon="🚨")
    else:
        st.caption(f":blue[Playlist name:] _{playlist_info['playlist_name']}_")
        playlist_size = len(playlist_info['tracks'])
        st.caption(f":blue[Number of tracks:] _{playlist_size}_")
        # Create a placeholder for the button
        button_placeholder = st.empty()
        if (playlist_size <= 30):
            # Check if the "Download All" button should be shown
            if button_placeholder.button('Download Playlist'):
                print('Load mp3 files')
                button_placeholder.empty()  # Remove the old button
                if button_placeholder.button('Download All'):  # Show the "Download All" button
                    print('download filezzz')
        else:
            st.warning("Playlist is too big!", icon="⚠️")


