# Arré
A collection of quick-and-dirty Python script to download and transcribe [trials from the Radio Radicale archives](https://www.radioradicale.it/processi) (feel free to skip the rambling and go directly to [the practicalities](#dependencies)).

## Goals and design philosophy
This is a holiday NLP project I started because of my mother and my cousin's desire to make a high-quality transcription of my grandfather's interventions in a few trials that were important for the history of Italy without spending the rest of their lives manually transcribing every single word.

The final product should be a relatively user-friendly tool that:
- [x] downloads the apparently undownloadable audio recordings of the debates
- [x] breaks them down into more manageable chunks, separating speech from non-speech segments (stretch goal: diarization)
- [x] provides a decent first draft of a transcript (stretch goal: punctuation restoration). Results are by no means expected to be perfect, but they should be helpful rather than confusing like Radio Radicale's automatic captions
- [ ] allows users to interactively refine the transcript (stretch goal: making the system "learn", to some extent and not necessarily as in "machine learning", from past mistakes)
- [ ] generates LaTeX code to easily obtain the transcription as a nicely typeset PDF 

For these reasons, I tried to keep the following in mind:

- __this is going to run on (old) laptops__: it's OK to wait for a little while, but the whole thing should not be unreasonably slow. In particular, this means that:
  - I cannot train any models, even if I have the data (which I don't, not really)
  - in general, much faster is better than slightly more accurate
  - even if I like running everything locally, if offline ASR tools don't work it's okay to use REST APIs (see below)
- __we are not paid for this, and we should not pay for this__: speaking of APIs, I really think [Google Cloud Speech](https://cloud.google.com/speech/) would do a better job than Google Speech Recognition, but the latter has the priceless (pun intended) advantage of being free
- __my mum is going to use this software__: 
  - I'm not gonna go all-in and develop a GUI, but using the interactive transcription program should not require a Master's in Computer Science
  - the editor and the media player should be easy to get used to, if not familiar, and the format of the human-edited `.txt` files should be as simple as possible
  - usage instruction should be available in Italian
- __this is not a research project__: I don't care whether [fullstop-deep-punctuation-prediction](https://github.com/oliverguhr/fullstop-deep-punctuation-prediction) is state-of-the-art or not. If a package is easy to use and improves the results, it's in
- __this is, in fact, a holiday project__: I have both more fun things to do while at the seaside and more interesting NLP projects to focus on when I'm back at work. So, no headaches allowed: if A is too complicated, replace it with B.

### Naming
I named the project _arré_, the Sicilian word for "again", not only because my family, my grandfather included, is from Sicily, and pointing to the Italian term _arringa_ ("closing argument" in the legal domain), but also thinking of one of the problems I was anticipating when I started thinking about automatically transcribing long audio files: that of systematic errors.
I could easily picture myself my mother, seeing the same uncommon surname misspelled for the 15th time, exclaiming "Arre!?!" and getting angry (with good reason) at the computer. 
In the development of this tool, I'm trying hard (but not as hard as I possibly can) to prevent this from happening too much.
If I fail, I guess this will be at least well named :)

## Dependencies
This program requires the Python dependencies listed in [`dependencies.txt`](dependencies.txt) and some external software tools:

- ffmpeg
- an audio player (__at the moment, only VLC is supported__)
- a text editor (__at the moment, only Mousepad is supported__)

Note that this program has only been tested on Manjaro Linux. Eventually, it will also run on Ubuntu and Windows.

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
      - `simple-segment`: simple speech-nonspeech segmentation with [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter) (fast)
4. (optional) Ttranscribe the trial with [`transcribe.py`](transcribe.py). Usage is as follows:
   ```
   python transcribe.py CMD WAV_PATH [--no-punct]
   ```
   where `CMD` can be `google` or `sphinx`. 
   This is an interactive process: segment by segment, you will be able to listen to read the automatic transcription of the trial and make corrections and adjustments. Each segment's transcription is stored in a separate file, named `START-STOP.txt`, so that you can quit the program at any time to then continue from the following segment.
   Guidelines on how to transcribe are given in [`transcribing.md`](transcribing.md).
   Note that:
   - `google` uses Google Speech Recognition (not to be confused with the more advanced, paid [Google Cloud Speech API](https://cloud.google.com/speech/)). It has a fairly good language model for Italian and requires a working internet connection
   - `sphinx` uses [CMUSphinx](https://cmusphinx.github.io/wiki/). On paper, this is a better tool for the job: it is highly configurable, it supports custom keywords and it even works offline! In practice, unfortunately, I could never get it to work despite doing all the necessary boring setup described above. You're very welcome to show me what I am doing wrong.
   By default, the system will try to restore punctuation using [a pretty cool, rather recent Python package](https://github.com/oliverguhr/fullstop-deep-punctuation-prediction). If you find this unhelpful, you can add the `--no-punct` flag __after the `SEGMENT_START` and `SEGMENT_END` arguments__ (quick-and-dirty means, among other things, that I decided not to waste my time with `argparse`).
5. TODO: generate the PDF