import sys
import speech_recognition as sr
import deepmultilingualpunctuation as dmp

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

def restore_punctuation(transcription):
    return dmp.PunctuationModel().restore_punctuation(transcription)

if __name__ == "__main__":
    cmd = sys.argv[1]
    audio_path = sys.argv[2]
    start = float(sys.argv[3])
    stop = float(sys.argv[4])
    if cmd == "sphinx":
        transcription = transcribe_segment_sphinx(audio_path, start, stop)
    elif cmd == "google":
        transcription = transcribe_segment_google(audio_path, start, stop)
    if transcription: 
        if len(sys.argv) > 5 and sys.argv[5] == "--no-punct":
            print("\n\t>", transcription)
        else:
            print("\n\t>", restore_punctuation(transcription))
    else:
        print("Invalid transcription method!")
        