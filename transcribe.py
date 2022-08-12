from email.mime import audio
import sys
import csv
import speech_recognition as sr

def transcribe_segment(audio_path, start, stop, hints=[]):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = r.record(source, offset=start, duration=stop - start)
        return r.recognize_sphinx(
                audio, 
                language="it-IT", 
                keyword_entries=hints)


if __name__ == "__main__":
    trial = sys.argv[1]
    pass