import os
import sys
from matplotlib import interactive
import speech_recognition as sr
import deepmultilingualpunctuation as dmp
import csv
from play import play_segment_vlc
import preventable_errors as pe

def transcribe_segment_sphinx(audio_path, start, stop, hints=[]):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = r.record(source, offset=start, duration=stop - start)
    try: 
        transcription = r.recognize_sphinx(
            audio, 
            language="it-IT", 
            keyword_entries=hints)
    except sr.RequestError:
        print("API unavailable")
        transcription = ""
    except sr.UnknownValueError:
        print("Unintellegible speech")
        transcription = "(incomprensibile)"
    return transcription


def transcribe_segment_google(audio_path, start, stop):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = r.record(source, offset=start, duration=stop - start)
    try:
        transcription = r.recognize_google(audio, language="it-IT")
    except sr.RequestError:
        print("API unavailable")
        transcription = ""
    except sr.UnknownValueError:
        print("Unintellegible speech")
        transcription = "(incomprensibile)"
    return transcription

def prevent_errors(prev_errs, transcription):
    for word in transcription.split():
        if word in prev_errs.keys():
            transcription.replace(
                str(prev_errs[word].append(word)).replace(", ","|")
                )
    return transcription
        

def restore_punctuation(transcription):
    return dmp.PunctuationModel().restore_punctuation(transcription)

def interactive_transcribe_segment(cmd, audio_path, txt_path, start, stop, punct=True, prev_errs={}):
    # transcribe
    if cmd == "sphinx":
        transcription = transcribe_segment_sphinx(audio_path, start, stop)
    elif cmd == "google":
        transcription = transcribe_segment_google(audio_path, start, stop)
    else:
        print("Invalid transcription method!")
        exit(1)

    # apply preventable error suggestions
    transcription = prevent_errors(prev_errs, transcription)

    # restore punctuation
    if punct:
        try:
            transcription = restore_punctuation(transcription)
        except: # happens e.g. if transcription = "" 
            pass

    # write transcription to txt file
    with open(txt_path, "w") as f:
        f.write(transcription)

    # play fragment; creates a tmp.wav file to be deleted/overwritten
    play_segment_vlc(audio_path, start, stop) 

    # open txt file in text editor
    res = os.system("mousepad " + txt_path) # TODO: separate Windows command
    if res == 0:
        return

def interactive_transcribe_trial(cmd, audio_path, json_path, punct=True):
    # init preventable errors
    prev_errs = {}
    if os.path.exists(json_path):
        prev_errs = pe.read_prev_errs(json_path) 

    # read segments from CSV
    csv_path = os.path.join(os.path.dirname(audio_path), "segments.csv")
    with open(csv_path) as f:
        segments = csv.reader(f, delimiter="\t")
        for (label,start_str,stop_str) in list(segments):
            txt_path = os.path.join(
                os.path.dirname(audio_path), 
                start_str + "-" + stop_str + ".txt"
            )
            if not os.path.exists(txt_path): # start where you left off
                if label == "speech":

                    # do the autotranscribing
                    interactive_transcribe_segment(
                        cmd, 
                        audio_path, 
                        txt_path,
                        float(start_str), 
                        float(stop_str), 
                        punct,
                        prev_errs
                        )

                    # update preventable errors
                    prev_errs = pe.extract_prev_errs(
                        prev_errs, 
                        txt_path, 
                        json_path)
                    
                elif label == "pause": # TODO: make pauses human-checkable
                    pass
        

if __name__ == "__main__":
    cmd = sys.argv[1]
    audio_path = sys.argv[2]
    json_path = os.path.join(os.path.dirname(audio_path), "prev_errs.json")
    interactive_transcribe_trial(cmd, audio_path, json_path)
        