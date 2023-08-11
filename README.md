# Savify :notes:
Not a Spotify Premium user? Not a problem! With Savify, all you need is to provide a Spotify song URL and download the track with just one click.

Try [Savify](https://savify.streamlit.app)!

## How it works:
This web app makes use of 2 official APIs: [Spotify Web API](https://developer.spotify.com/documentation/web-api) and the [YouTube Data API](https://developers.google.com/youtube/v3) to fetch and retrieve music data. When the user enters a valid Spotify track URL, the program extracts its unique Spotify ID then makes the Spotify API call to retrieve its name and list of artists from the response, in the form of a dictionary, ```track_info```. This dictionary is crucial for this app as its contents are used practically for everything. 

The first and most important use of ```track_info``` is to actually retrieve an audio buffer of said track. Since Spotify provided us with the song title and artist names, the app then searches for the song on YouTube by using the YouTube Data API with the following search query: '[Artist names] - [Song name] (Audio)'

From the response, the app extracts the first search result's youtube video ID and constructs a [Pytube](https://pytube.io/en/latest/) YouTube object. Audio stream is then extracted and downloaded as an mp3 file.

## Limitations:
- Since the searching/sraping is being done strictly with the YouTube Web API, its daily quota restricts the amount of songs that can be found (hence downloaded) from YouTube.
- The search query  '[Artist names] - [Song name] (Audio)' might not work well for classical pieces that have a different way of being named (e.g: "10 Preludes , Op. 23: No.5 in G Minor: Allegro" by Sergei Rachmaninof -- Beautiful piece btw, you should absolutely [have a listen!](https://open.spotify.com/track/0zvOxmMNj1o8nNhn2LrmPp?si=8477188b873f43d5) )