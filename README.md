# Arrè
A collection of Python scripts to download and transcribe [recordings from the Radio Radicale archive](https://www.radioradicale.it/processi).

## Motivation
These scripts were written to facilitate a family project in the context of which we want to transcribe some of the arguments of my grandfather, lawyer Giuseppe Grillo (see status [here](status.md)).
Many important trials were aired on Radio Radicale and are now part of its archive.

The Radio Radicale website, however, no longer allows downloading the relevant audio tracks and its responsibles have not answered our repeated requests to obtain the files at hand, forcing us to ["record" the corresponding audio streams](#downloading-audio-recordings-from-radioradicaleit).

In addition, most recordings are at least one hour long, making it necessary for us to start from an automatic transcript (see [Transcribing audio recordings](#transcribing-audio-recordings)).

## Requirements
- Python 3.11 or 3.13 (other Python 3 versions might work too, but have not been tested)
- the [mpv](https://mpv.io/installation/) media player (necessary for the download step)

## Setup
1. Clone this repository
2. install the Python dependencies listed in [requirements.txt](requirements.txt). Using a virtual environment is highly recommended

## Usage

### Downloading audio recordings from radioradicale.it
Move inside the `arre` folder and run

```
python download.py WEBPAGE_URLs
```

where `WEBPAGE_URLs` is a list of URLs of Radio Radicale pages containing an RTSP stream, such as [this one](https://www.radioradicale.it/scheda/17807/maxiprocesso-a-cosa-nostra).

This script will create one or more folders `data/PAGE-TITLE` containing the audio track(s) in question.

> __NOTE:__ the "download" process takes a long time since the program needs to actually reproduce and "record" the entire RSTP audio stream. However, this process is lightweight and does not require the volume to be turned up. 

### Transcribing audio recordings
To transcribe an audio file, run

```
python transcribe.py PATH_TO_AUDIO_FILE
``` 

The result will be an `.srt` file, which will be placed in the same folder as the source audio track.

> __NOTE:__ This step uses a (relatively) small OpenAIs Whispe model, more specifically [stable-ts](https://github.com/jianfch/stable-ts). The prompt can be configured by editing the [whisper_prompt.txt file](whisper_prompt.txt). 

## Namesake
The Sicilian word _arrè_, meaning "again", was chosen because:

- my grandfather is from Agrigento, Sicily
- the word itself reminds of the Italian word _arringa_ (plea, argument), typical of the legal domain.
