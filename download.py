import sys
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import mpv

DATA_FOLDER = "data"

'''Given a trial webpage url, return the URL of the audio
stream it contains and its title'''
def get_stream(webpage_url):
    soup = BeautifulSoup(urlopen(webpage_url).read(), features="html.parser")
    streams = soup.find_all(title="Player")
    return [stream.get("href") for stream in streams], soup.title.string

'''Given a stream title and url, write the stream's audio contents to an 
mp3 file with mpv'''
def download_rtsp(stream_url, title):
    subdir_path = os.path.join(DATA_FOLDER, title)
    if not os.path.isdir(subdir_path): os.makedirs(subdir_path)
    player = mpv.MPV(
        stream_record = os.path.join(subdir_path, os.path.basename(stream_url)))
    player.play(stream_url)
    player.wait_for_playback()

if __name__ == "__main__":
    if not os.path.isdir(DATA_FOLDER): os.mkdir(DATA_FOLDER)
    webpage_urls = sys.argv[1:]
    for (i,webpage_url) in enumerate(webpage_urls):
        print("parsing page {} of {}...".format(i + 1, len(webpage_urls)))
        stream_urls, title = get_stream(webpage_url)
        for (i,stream_url) in enumerate(stream_urls):
            print("recording track {} of {}...".format(i + 1, len(stream_urls)))
            download_rtsp(stream_url,title)
