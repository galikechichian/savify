# Author: Gali Kechichian
# Backend script to extract tracks info from 
# Spotify playlist

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from re import search
import streamlit as st


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

@st.cache_data
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


def extract_track_id(track_url):
    """
    (str) -> str        -- No errors
    (str) -> NoneType   -- No match found, error
    Helper: given a Spotify URL, it returns a Spotify ID
    """
    pattern = r'track/([a-zA-Z0-9]+)'
    match = search(pattern, track_url)
    if match:
        track_id = match.group(1)
        return track_id
    else:
        return None


@st.cache_data
def get_playlist(token, link):
    """
    Makes Spotify Web API call to get server response
    (Get Playlist by its Spotify URL)
    """
    sp_id = extract_playlist_id(link)
    headers = get_auth_header(token)
    query_url = f"https://api.spotify.com/v1/playlists/{sp_id}"
    response = get(query_url, headers=headers)
    return response


@st.cache_data
def get_track(token, link):
    """
    Makes Spotify Web API call to get server response
    (Get Playlist by its Spotify URL)
    """
    sp_id = extract_track_id(link)
    headers = get_auth_header(token)
    query_url = f"https://api.spotify.com/v1/tracks/{sp_id}"
    response = get(query_url, headers=headers)
    return response


def got_error(response):
    """
    (response) -> bool
    returns True if API call didn't result in errros,
    False otherwise
    """
    return (response.status_code != 200)


def get_playlist_info(response):
    """
    (response) -> str           -- For error messages
    or 
    (response) -> list(tuples)  -- For track info

    Helper that filters response into a dictionary:
    playlist_info = {
        "error_message": error message
        "playlist_name: name
        "tracks": [
            (artists, name),
            (artists, name),
            ...
        ]
    }
    0 -> artists
    1 -> song name
    2 -> duration in ms
    """
    playlist_info = {
        "error_message": "",
        "playlist_name": "",
        "tracks": [] # (artists.name, name ), (), ...
    }
    json_result = json.loads(response.content)
    
    if got_error(response): # got an error
        return json_result["error"]["message"]
        
    # no errors, load playlist
    playlist_info["error_message"] = None
    playlist_info["playlist_name"] = json_result["name"]
    for sp_item in json_result["tracks"]["items"]:
        # extract info for each item
        # to handle unexpected NoneType items
        if sp_item['track'] == None:
            continue

        artists = sp_item['track']['artists']
        artist_names = []
        for artist in artists:
            artist_names.append(artist['name'])
        name = sp_item['track']['name']
        playlist_info["tracks"].append((artist_names, name))
            
    return playlist_info


def get_track_info(_response):
    """
    (response) -> str           -- For error messages
    or 
    (response) -> list(tuples)  -- For track info

    Helper that filters response into a dictionary:
    track_info = {
        "error_message": error message
        "artists": [artist0, artist1, ...]
        "name": name
    }
    """
    track_info = {
        "error_message": "",
        "artists": [],
        "name": []
    }
    json_result = json.loads(_response.content)
    
    if got_error(_response): # got an error
        return json_result["error"]["message"]
        
    # no errors, load playlist
    track_info["error_message"] = None
    artists = []
    for artist in json_result["artists"]:
        artists.append(artist["name"])
    track_info["artists"] = artists
    track_info["name"] = json_result["name"]  
    # print("ran 'get track info'")             # testing if caching worked
    return track_info
