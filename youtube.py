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

request = youtube.search().list(
    part="snippet",
    maxResults=1,
    q="Agua de Beber"
)
response = request.execute()


print(response)
