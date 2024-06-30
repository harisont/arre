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
    a = soup.find(title="Player")
    return a.get("href"), soup.title.string

'''Given a stream title and url, write the stream's audio contents to an 
mp3 file with mpv'''
def download_rtsp(stream_url, title):
    subdir_path = os.path.join(DATA_FOLDER, title)
    if not os.path.isdir(subdir_path): os.makedirs(subdir_path)
    player = mpv.MPV(
        # TODO: adapt for non-mp3 files (from stream extension)
        stream_record = os.path.join(subdir_path, 'audio.mp3'))
    player.play(stream_url)
    player.wait_for_playback()

if __name__ == "__main__":
    if not os.path.isdir(DATA_FOLDER): os.mkdir(DATA_FOLDER)
    for webpage_url in sys.argv[1:]:
        stream_url, title = get_stream(webpage_url)
        download_rtsp(stream_url,title)
