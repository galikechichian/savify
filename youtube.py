import os
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
from pytube import YouTube
from pathlib import Path
from requests import get
from bs4 import BeautifulSoup

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
api_service_name = "youtube"
api_version = "v3"


youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)


def make_search_query(artists, name):
    """
    (list, str) -> str
    Given the artist names and song title, returns search query string
    """
    artist_str = ', '.join(artists)
    query = f'{artist_str} - {name} (Audio)'
    return query


def search_song(query):
    """
    (str) -> str
    Given a search query string, scrapes for the 1st result 
    on YouTube and returns its Video ID
    ***
    (query) -> video ID -- No errors
    (query) -> 1        -- Result isn't a simple video
    (query) -> 2        -- No results
    """
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
    return video_dict


def get_video_id(query):
    """
    (str) -> str        -- No issues, video is found
    (str) -> 1          -- Couldn't find requested video
    Takes search query string as input
    Returns YouTube Video ID
    """
    video_dict = search_song(query)
    if video_dict == None:
        return None
    video_id = video_dict["id"]["videoId"]
    return video_id


def get_video_url(video_id):
    """
    (str) -> str               -- No issues, video found
    (str) -> None              -- Video not found, proceed with caution :p
    Takes video ID as input
    Returns its youtube URL
    """
    return f"https://www.youtube.com/watch?v={video_id}"


def make_yt_obj(video_url):
    """
    (str) -> YouTube        -- No issues
    (str) -> None           -- Video not found
    """
    if video_url != None:
        yt = YouTube(video_url)
        return yt
    return None


def get_yt_stream(video_url):
    """
    (str) -> stream                 -- No errors
    (str) -> None                   -- Stream not found
    Gets stream from YouTube URL
    """
    yt = make_yt_obj(video_url)
    if yt != None:
        stream = yt.streams.filter(only_audio=True).first()
        return stream


def get_filesize(stream):
    """
    (stream) -> float           -- No errors
    (stream) -> None    `       -- Stream not found
    Returns file size in MB
    """
    if stream != None:
        return stream.filesize_mb
    

def get_downloads_path():
    user_home = str(Path.home())
    downloads_path = os.path.join(user_home, "Downloads")
    return downloads_path


def donwnload_video(stream, playlist_name, artists, name):
    """
    (stream) -> str
    Downloads youtube video as mp3 in downloads folder
    returns video path
    """
    if stream != None:
        # To make mp3 file
        filename = f"{', '.join(artists)} - {name}.mp3"
        downloads_path = get_downloads_path() + f"/{playlist_name}"
        video_path = stream.download(output_path=downloads_path, filename=filename)
        return video_path


# artists = ['Madison Beer']
# name = 'Good in Goodbye'
# playlist_name = 'playlist'
# vid_id = get_video_id(make_search_query(artists, name))
# vid_url = get_video_url(vid_id)
# stream = get_yt_stream(vid_url)
# donwnload_video(stream, playlist_name, artists, name)


def get_search_url(query):
    return f"https://www.google.com/search?q={query}"


# def get_google_search_result(query):
#     url = get_search_url(query)
#     response = get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     print(soup.prettify())


from spotify import *

url = "https://open.spotify.com/playlist/2ayG6c4x18YP6E7CVKP3n4?si=d956b4ed276e46b9"
playlist_info = get_playlist_info(get_playlist(token, url))
q = make_search_query(playlist_info["tracks"][0][0], playlist_info["tracks"][0][1])


# artists = ['Madison Beer']
# name = 'Good in Goodbye'
# query = make_song_search_query(artists, name)
# yt_results = get_yt_results(query)