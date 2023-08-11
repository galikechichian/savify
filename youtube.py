import os
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
from pytube import YouTube
import streamlit as st
from io import BytesIO

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
api_service_name = "youtube"
api_version = "v3"


youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)


def make_search_query(track_info):
    """
    (dict) -> str
    (str)  -> None
    Given the artist names and song title, returns search query string
    """
    if type(track_info) == str:
        return None
    name = track_info["name"]
    artist_str = ', '.join(track_info["artists"])
    query = f'{artist_str} - {name} (Audio)'
    return query


@st.cache_data(show_spinner=False)
def search_song(track_info):
    """
    (dict) -> str
    Given a search query string, scrapes for the 1st result 
    on YouTube and returns its Video ID
    ***
    (query) -> video ID -- No errors
    (query) -> 1        -- Result isn't a simple video
    (query) -> 2        -- No results
    """
    query = make_search_query(track_info)
    if query == None:
        return None
    
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    response = request.execute()
    if response == None:
        return None
    video_dict = response["items"][0]
    if video_dict["id"]["kind"] != 'youtube#video':
        return None 
    # print('made api call')
    return video_dict


def get_video_id(track_info):
    """
    (dict) -> str        -- No issues, video is found
    (dict) -> 1          -- Couldn't find requested video
    Takes search query string as input
    Returns YouTube Video ID
    """
    video_dict = search_song(track_info)
    if video_dict == None:
        return None
    video_id = video_dict["id"]["videoId"]
    # print(f"Video ID: {video_id}")
    return video_id


def make_yt_obj(track_info):
    """
    (dict) -> YouTube        -- No issues
    (dict) -> None           -- Video not found
    """
    # video_url = get_video_url(track_info)
    video_id = get_video_id(track_info)
    if video_id != None:
        yt = YouTube.from_id(video_id)
        return yt
    return None


def get_yt_stream(track_info):
    """
    (dict) -> stream                 -- No errors
    (dict) -> None                   -- Stream not found
    Gets stream from YouTube URL
    """
    yt = make_yt_obj(track_info)
    if yt != None:
        stream = yt.streams.get_audio_only()
        return stream


def get_filesize(track_info):
    """
    (stream) -> float           -- No errors
    (stream) -> None    `       -- Stream not found
    Returns file size in MB
    """
    stream = get_yt_stream(track_info)
    if stream != None:
        return stream._filesize_mb
    return None


def get_filename(track_info):
    """
    (dict) -> str
    Takes in track info dictionary, returns the filename
    that would be used to download it
    """
    artists = track_info['artists']
    name = track_info['name']
    filename = f"{', '.join(artists)} - {name}.mp3"
    return filename


@st.cache_data(show_spinner=False)
def download_audio_to_buffer(track_info):
    """
    (stream) -> BytesIO
    Takes track info as input
    Returns audio buffer
    """
    buffer = BytesIO()
    stream = get_yt_stream(track_info)
    if stream != None:
        stream.stream_to_buffer(buffer)
        return buffer
    return None