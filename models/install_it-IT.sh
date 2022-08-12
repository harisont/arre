#!/usr/bin/env bash

# code from https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst
SR_LIB=$(python -c "import speech_recognition as sr, os.path as p; print(p.dirname(sr.__file__))")
sudo unzip -o it-IT.zip -d "$SR_LIB"
sudo chmod --recursive a+r "$SR_LIB/pocketsphinx-data/it-IT/"