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

@st.cache_data(show_spinner=False)
def get_track(sp_id):
    """
    Makes Spotify Web API call to get server response
    (Get Playlist by its Spotify URL)
    """
    token = get_token()
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


def get_track_info(_response):
    """
    (response) -> dict           -- For track info
    (response) -> str             -- For errors

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
    return track_info
