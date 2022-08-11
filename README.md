# Arré
A collection of quick-and-dirty Python script to download and transcribe [trials from the Radio Radicale archives](https://www.radioradicale.it/processi).

## Usage
1. Download the MP3 file(s) with [`download.py`](download.py) to the current folder. Run
    ```
    python download.py WEBPAGE_URL(s)
    ```
   where `WEBPAGE_URL` is a Radio Radicale URL containing an RTSP stream, such as [this one](https://www.radioradicale.it/scheda/17807/maxiprocesso-a-cosa-nostra).
   This is a very long process, as most audio files are not directly available for download anymore, making it necessary to "record" them with [ffmpeg](https://pypi.org/project/python-ffmpeg/). So, downloading a 1h30m file takes approximately 1h30m.
2. Convert them to WAV with [`convert.py`](convert.py), i.e. run
    ```
    python convert.py MP3_PATH(s)
    ```
3. Segment the WAV files [`segment.py`](segment.py), running
    ```
    python segmetn.py CMD WAV_PATH(s)
    ```
    Here, `CMD` is used to specify the segmentation method. The available methods are:
       - `pyannote-audio`: speaker diarization with [pyannote-audio](https://github.com/pyannote/pyannote-audio) (way too slow to be suitable for a laptop with no GPU)
       -  `inaSpeechSegmenter`: speech-noise-noEnergy segmentation with [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter) (fast)
       -  `pyAudioAnalysis`: speaker diarization with [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) (very slow)