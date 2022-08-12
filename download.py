from urllib.request import urlopen
from bs4 import BeautifulSoup
from ffmpeg import FFmpeg
import asyncio
import sys
import os

DATA_FOLDER = "data"
TMP = "tmp.mp3"

'''Given a trial webpage url, return the URL of the audio
stream it contains and its title'''
def get_stream(webpage_url):
    soup = BeautifulSoup(urlopen(webpage_url).read())
    a = soup.find(title="Player")
    return a.get("href"), soup.title.string

'''Given a stream title and url, write the stream's audio contents to an 
mp3 file with FFMPEG'''
def download_rtsp(stream_url, title):
    subdir_path = os.path.join(DATA_FOLDER, title)
    if not os.path.isdir(subdir_path): os.makedirs(subdir_path)
    ffmpeg = FFmpeg().input(
        stream_url,
    ).output(
        TMP,
        {'codec:v': 'copy'},
    )

    @ffmpeg.on('start')
    def on_start(arguments):
        print('Started stream download...')

    @ffmpeg.on('stderr')
    def on_stderr(line):
        print('stderr:', line)

    @ffmpeg.on('progress')
    def on_progress(progress):
        print(progress)

    @ffmpeg.on('completed')
    def on_completed():
        print('Completed stream download!')

    @ffmpeg.on('terminated')
    def on_terminated():
        print('Terminated stream download.')

    @ffmpeg.on('error')
    def on_error(code):
        print('Error: ', code)

    asyncio.run(ffmpeg.execute())
    os.rename(TMP, os.path.join(subdir_path, 'full_audio.mp3'))

if __name__ == "__main__":
    if not os.path.isdir(DATA_FOLDER): os.mkdir(DATA_FOLDER)
    for webpage_url in sys.argv[1:]:
        stream_url, title = get_stream(webpage_url)
        download_rtsp(stream_url,title)
