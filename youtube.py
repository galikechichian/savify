import os
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
from pytube import YouTube

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

def donwnload_video(stream):
    """
    (stream) -> None
    """
    if stream != None:
        stream.download()


artists = ['Andy Powell']
name = 'Love, Lies & Flipsides'
vid_id = get_video_id(make_search_query(artists, name))
vid_url = get_video_url(vid_id)
stream = get_yt_stream(vid_url)
donwnload_video(stream)

