# Author: Gali Kechichian
# Main script
from spotify import *
from youtube import *
import streamlit as st

st.set_page_config(
    page_title='Savify',
    page_icon=":musical_notes: "
    )

def space(): 
    st.write('\n\n')

st.title("Savify")
st.header("Enjoy your favorite Spotify songs offline.")

space()

st.write('1. Go to Spotify and copy the song URL\n2. Paste it in the box below and convert to MP3\n3. Donwload track on your device\n4. Enjoy your music offline!')


space()

song_link = st.text_input(
    "Enter a valid Spotify song URL:", 
    placeholder="Example: https://open.spotify.com/track/58sxA5EEjq57yGggwThArx?si=edf556a1afcb4ab3",
    )

if song_link:
    with st.spinner("Loading your song..."):
        try:
            response = get_track(extract_track_id(song_link))
            track_info = get_track_info(response)
        except:
            st.error('An error occurred white fetching the song. Please try again.')


    if (got_error(response)):
        st.error(track_info, icon="🚨")
    else:
        st.caption(f"{', '.join(track_info['artists'])} - {track_info['name']}")
        button_container = st.empty()
        button_label = 'Convert to MP3'
        if button_container.button(button_label):
            with st.spinner("Converting audio..."):
                try:
                    buffer = download_audio_to_buffer(track_info)
                    filesize = get_filesize(track_info)
                    filename = get_filename(track_info)
                    st.success(f"Conversion successful! File size: {filesize}Mb")
                    button_container.empty()
                    st.download_button(
                        label="Download MP3 File",
                        data=buffer,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
                except:
                    st.error('An error occurred. Please try again.')
        