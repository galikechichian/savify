# Author: Gali Kechichian
# Backend script
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from re import search
from pytube import YouTube
import savify

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def extract_playlist_id(playlist_url):
    """
    (str) -> str        -- No errors
    (str) -> NoneType   -- No match found, error
    Helper: given a Spotify URL, it returns a Spotify ID
    """
    pattern = r'playlist/([a-zA-Z0-9]+)'
    match = search(pattern, playlist_url)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        return None
    

def get_playlist(token, link):
    """
    Makes Spotify Web API call to get server response
    (Get Playlist by its Spotify URL)
    """
    sp_id = extract_playlist_id(link)
    headers = get_auth_header(token)
    query_url = f"https://api.spotify.com/v1/playlists/{sp_id}/tracks"
    response = get(query_url, headers=headers)
    return response


def got_error(response):
    """
    (response) -> bool
    returns True if API call didn't result in errros,
    False otherwise
    """
    return (response.status_code != 200)


def get_tracks(response):
    """
    (response) -> str           -- For error messages
    or 
    (response) -> list(tuples)  -- For track info

    Helper that filters response into a dictionary:
    playlist_info = {
        "error_message": error message
        "tracks": [
            (artists, name, duration),
            (artists, name, duration),
            ...
        ]
    }
    0 -> artists
    1 -> song name
    2 -> duration in ms
    """
    playlist_info = {
        "error_message": "",
        "tracks": [] # (artists.name, name ), (), ...
    }
    json_result = json.loads(response.content)
    
    if got_error(response): # got an error
        return json_result["error"]["message"]
        
    # no errors, load playlist
    playlist_info["error_message"] = None
    for sp_item in json_result["items"]:
        # extract info for each item
        # to handle unexpected NoneType items
        if sp_item['track'] == None:
            continue

        artists = sp_item['track']['artists']
        artist_names = []
        for artist in artists:
            artist_names.append(artist['name'])
        name = sp_item['track']['name']
        duration = sp_item['track']['duration_ms']
        playlist_info["tracks"].append((artist_names, name, duration))
            
    print(playlist_info["tracks"])
    return playlist_info["tracks"]


token = get_token()

sample_link = "https://open.spotify.com/playlist/2ayG6c4x18YP6E7CVKP3n4?si=e8f0df37dcef447e"
sample_link2 = "https://open.spotify.com/playlist/63kAPbsf3EpKHQo6qMXrr7?si=6587d543aed7440c"
sample_link3 = "https://open.spotify.com/playlist/69SLmftyC6GplNTXdwM7uR?si=5c5864a75740479d"
dummy_link = "https://open.spotify.com/playlist/2ayG6c4x18YP6E7CVKP3n4?si=ba1b630d26f14cf1"
faulty_link = "https://open.spotify.com/plylist/4C7GEVUb58cxeSVRTFRC6?si=9be3e6a70bb84a98&pt=7d6454462cfb431fad5c361d4ecf6934"

# response = get_playlist(token, savify.playlist_link)
# get_tracks(response)


video = YouTube("http://youtu.be/mUs97qXjw1M")