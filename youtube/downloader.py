from pytube import YouTube
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from pytube.innertube import _default_clients

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

def download_youtube_video(url, output_path='.'):
    try:

        yt = YouTube(url,
                     use_oauth=True,
                     allow_oauth_cache=True)
        
        stream = yt.streams.get_highest_resolution()
        
        stream.download(output_path)
        
        print(f"Downloaded '{yt.title}' successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    video_url = 'https://www.youtube.com/watch?v=np79qHkkbZU'
    
    download_youtube_video(video_url, output_path='data/')
