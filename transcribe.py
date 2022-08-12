import sys
import speech_recognition as sr

def transcribe_segment_sphinx(audio_path, start, stop, hints=[]):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = r.record(source, offset=start, duration=stop - start)
    try: 
        txt = r.recognize_sphinx(
            audio, 
            language="it-IT", 
            keyword_entries=hints)
    except sr.RequestError:
        print("API unavailable")
        txt = ""
    except sr.UnknownValueError:
        print("Unintellegible speech")
        txt = "(incomprensibile)"
    return txt


def transcribe_segment_google(audio_path, start, stop):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio = r.record(source, offset=start, duration=stop - start)
    try:
        txt = r.recognize_google(audio, language="it-IT")
    except sr.RequestError:
        print("API unavailable")
        txt = ""
    except sr.UnknownValueError:
        print("Unintellegible speech")
        txt = "(incomprensibile)"
    return txt

if __name__ == "__main__":
    cmd = sys.argv[1]
    audio_path = sys.argv[2]
    start = float(sys.argv[3])
    stop = float(sys.argv[4])
    txt = "Invalid transcription method!"
    if cmd == "sphinx":
        txt = transcribe_segment_sphinx(audio_path, start, stop)
    elif cmd == "google":
        txt = transcribe_segment_google(audio_path, start, stop)
    print("\n\t>", txt)