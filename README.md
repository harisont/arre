# Arré
A collection of quick-and-dirty Python script to download and transcribe [trials from the Radio Radicale archives](https://www.radioradicale.it/processi).

## Usage
1. Download the audio file(s) with [`dl_audio.py`](dl_audio.py) to the current folder. Run
    ```
    python dl_audio.py WEBPAGE_URL(s)
    ```
   where `WEBPAGE_URL` is a Radio Radicale URL containing an RTSP stream, such as [this one](https://www.radioradicale.it/scheda/17807/maxiprocesso-a-cosa-nostra).
   This is a very long process, as most audio files are not directly available for download anymore, making it necessary to "record" them with [ffmpeg](https://pypi.org/project/python-ffmpeg/). So, downloading a 1h30m file takes approximately 1h30m.