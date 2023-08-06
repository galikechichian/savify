# Author: Gali Kechichian
# Backend script
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import re
from pytube import YouTube

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
    Helper: given a Spotify URL, it returns a Spotify ID
    """
    pattern = r'playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, playlist_url)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        return None
    

def get_tracks(result):
    """
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
    json_result = json.loads(result.content)
    
    if result.status_code != 200: 
        playlist_info["error_message"] = json_result["error"]["message"]
    else: 
        playlist_info["error_message"] = None
        
        for sp_item in json_result["items"]:
            artists = sp_item['track']['artists']
            
            artist_names = []
            for artist in artists:
                artist_names.append(artist['name'])
                print(artist_names)
            
            name = sp_item['track']['name']
            duration = sp_item['track']['duration_ms']
            playlist_info["tracks"].append((artist_names, name, duration))

    print(playlist_info["tracks"])
    return playlist_info["tracks"]


def get_playlist(token, link):
    """
    Makes Spotify Web API call to get server response
    (Get Playlist by its Spotify URL)
    """
    sp_id = extract_playlist_id(link)
    headers = get_auth_header(token)
    query_url = f"https://api.spotify.com/v1/playlists/{sp_id}/tracks"
    result = get(query_url, headers=headers)
    return result
    

token = get_token()

sample_link = "https://open.spotify.com/playlist/63kAPbsf3EpKHQo6qMXrr7?si=a84288ecf7924cda"
get_tracks(get_playlist(token, sample_link))


video = YouTube("http://youtu.be/mUs97qXjw1M")

