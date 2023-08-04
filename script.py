from pytube import YouTube

link = input("Enter Youtube URL: ")
video = YouTube(link)

print(video.author)