# Author: Gali Kechichian
# Main script
from spotify import *
# from youtube import *
import streamlit as st

def space(): 
    st.write('\n\n')

st.title("Savify.")
st.subheader("Enjoy your favorite Spotify songs offline.")

space()

song_link = st.text_input(
    "Enter a valid Spotify song URL:", 
    placeholder="Paste URL here"
    # help="- Must be public\n- No more than 30 tracks",
    )


if song_link != "":
    response = ""
    with st.spinner("Loading your song..."):
        response = get_track(token, song_link)
        track_info = get_track_info(get_track(token, song_link))
    
    if (got_error(response)):
        st.error(track_info, icon="🚨")
    else:
        st.caption(f"Song: _{track_info['name']}_")
        st.caption(f"Artist(s): _{', '.join(track_info['artists'])}_")
        # Create a placeholder for the button
        button_placeholder = st.empty()
        # Check if the "Download All" button should be shown
        if button_placeholder.button('Download Song'):
            # print('Load mp3 files')
            print(1)


