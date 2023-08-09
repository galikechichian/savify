import os
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
from pytube import YouTube
from pathlib import Path
import streamlit as st

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

@st.cache_data
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
    print('made api call')
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
    return video_id


def get_video_url(track_info):
    """
    (dict) -> str               -- No issues, video found
    (dict) -> None              -- Video not found, proceed with caution :p
    Takes video ID as input
    Returns its youtube URL
    """
    video_id = get_video_id(track_info)
    return f"https://www.youtube.com/watch?v={video_id}"


def make_yt_obj(track_info):
    """
    (dict) -> YouTube        -- No issues
    (dict) -> None           -- Video not found
    """
    video_url = get_video_url(track_info)
    if video_url != None:
        yt = YouTube(video_url)
        return yt
    return None


def get_yt_stream(track_info):
    """
    (dict) -> stream                 -- No errors
    (dict) -> None                   -- Stream not found
    Gets stream from YouTube URL
    """
    video_url = get_video_url(track_info)
    print(video_url)
    yt = make_yt_obj(video_url)
    if yt != None:
        stream = yt.streams.filter(only_audio=True).first()
        return stream


def get_filesize(video_url):
    """
    (stream) -> float           -- No errors
    (stream) -> None    `       -- Stream not found
    Returns file size in MB
    """
    stream = get_yt_stream(video_url)
    if stream != None:
        return stream.filesize_mb
    

def get_downloads_path():
    user_home = str(Path.home())
    downloads_path = os.path.join(user_home, "Downloads")
    return downloads_path


def temp_dl(track_info):
    """
    (stream) -> str
    Downloads youtube video as mp3 in downloads folder
    returns filename
    """
    stream = get_yt_stream(track_info)
    artists = track_info['artists']
    name = track_info['name']
    if stream != None:
        # To make mp3 file
        filename = f"{', '.join(artists)} - {name}.mp3"
        # downloads_path = get_downloads_path()
        # video_path = stream.download(output_path=downloads_path, filename=filename)
        stream.download(output_path="temp", filename=filename)
        return filename
    

# @st.cache_resource
def download_track(track_info):
    filename = temp_dl(track_info)
    # st.success("MP3 Download Complete!")
    # st.download_button(
    #     "Download Track", 
    #     data=open(f"temp/{filename}", "rb").read(),
    #     file_name=filename
    #     )
    # st.cache_resource.clear()


def get_search_url(query):
    return f"https://www.google.com/search?q={query}"