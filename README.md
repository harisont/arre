# Arré
A collection of quick-and-dirty Python script to download and transcribe [trials from the Radio Radicale archives](https://www.radioradicale.it/processi).

## Dependencies
- the Python dependencies listed in [`dependencies.txt`](dependencies.txt)
- `ffmpeg`
- `unzip` (only if you are trying to transcribe with Sphinx, see below)

## Setup
1. Install the above listed dependencies
2. If you want to try using Sphinx for transcriptions (not recommended):
   1. [download the language models for Italian](https://drive.google.com/file/d/0Bw_EqP-hnaFNSXUtMm8tRkdUejg/view?resourcekey=0-9IOo0qEMHOAR3z6rzIqgBg) to the [`models`](models/) directory
   2. install them by running
        ```
        cd models && bash install_it-IT.sh 
        ```

## Usage
1. Download the MP3 file(s) with [`download.py`](download.py) to the `data` folder. Run
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
       - `diarize`: speaker diarization with [pyannote-audio](https://github.com/pyannote/pyannote-audio) (way too slow to be suitable for a laptop with no GPU and therefore untested)
       -  `simple-segment`: simple speech-nonspeech segmentation with [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter) (fast)
4. (optional) Test the different transcription methods __on individual segments__ using [`play.py`](play.py) and [`transcribe.py`](transcribe.py). Usage is as follows:
   ```
   python play.py WAV_PATH SEGMENT_START SEGMENT_END    # play the given segment
   ```
   where `SEGMENT_START` and `SEGMENT_END` are floating-point numbers, and, similarly,
   ```
   python transcribe.py CMD WAV_PATH SEGMENT_START SEGMENT_END
   ```
   where `CMD` can be `google` or `sphinx`. Note that:
   - `google` uses Google Speech Recognition (not to be confused with the more advanced, paid [Google Cloud Speech API](https://cloud.google.com/speech/)). It has a fairly good language model for Italian and requires a working internet connection
   - `sphinx` uses [CMUSphinx](https://cmusphinx.github.io/wiki/). On paper, this is a better tool for the job: it is highly configurable, it supports custom keywords and it even works offline! In practice, unfortunately, I could never get it to work despite doing all the necessary boring setup described above. You're very welcome to show me what I am doing wrong.
5. TODO: transcribe a trial!
6. TODO: generate the PDF