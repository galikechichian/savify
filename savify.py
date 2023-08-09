# Author: Gali Kechichian
# Main script
from spotify import *
from youtube import *
import streamlit as st
import re

token = get_token()

def space(): 
    st.write('\n\n')

st.title("Savify.")
st.subheader("Enjoy your favorite Spotify songs offline.")

space()

song_link = st.text_input(
    "Enter a valid Spotify song URL:", 
    placeholder="Example: https://open.spotify.com/track/58sxA5EEjq57yGggwThArx?si=edf556a1afcb4ab3"
    # help="- Must be public\n- No more than 30 tracks",
    )


if song_link != "":
    response = ""
    with st.spinner("Loading your song..."):
        response = get_track(token, song_link)
        track_info = get_track_info(response)
    
    if (got_error(response)):
        st.error(track_info, icon="🚨")
    else:
        st.caption(f"Song: _{track_info['name']}_")
        st.caption(f"Artist(s): _{', '.join(track_info['artists'])}_")

        if st.button('Donwload Track'):
            # st.write(track_info)
            # download_track(track_info)
            # print('***')
            # print(re.match(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", get_video_url(track_info)))
            # print()
            print(1)
