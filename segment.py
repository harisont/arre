import sys
import csv
from os import path
from pyannote.audio import Pipeline
from inaSpeechSegmenter import Segmenter
from pyAudioAnalysis import audioSegmentation

# Diarization with pyannote-audio (too slow to be useful)

'''Given its path, diarize a .wav file, returning a list of audio segments,
   audio_path needs to point to a .wav file'''
def diarize_pa(audio_path):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    diarization = pipeline(audio_path)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append([speaker, turn.start, turn.end])
    return segments

'''Write segments to a .csv file with the given title'''
def segments_to_csv_pa(title, segments):
    fields = ["label", "start", "stop"]
    with open(title + ".csv", 'w') as f:
        write = csv.writer(f, delimiter="\t")      
        write.writerow(fields)
        write.writerows(segments)

# Segmentation with inaSpeechSegmenter

def segment_ina(audio_path):
    segmenter = Segmenter(detect_gender=False)
    return segmenter(audio_path)

# Diarization with pyAudioAnalysis

def diarize_paa(audio_path):
    segments = audioSegmentation.speaker_diarization(audio_path, 0)
    return segments

if __name__ == "__main__":
    cmd = sys.argv[1]
    for audio_path in sys.argv[2:]:
        if cmd == "pyannote-audio":
            segments = diarize_pa(audio_path)
            segments_to_csv_pa(path.splitext(audio_path)[0], segments)
        elif cmd == "inaSpeechSegmenter":
            segments = segment_ina(audio_path)
            segments_to_csv_pa(path.splitext(audio_path)[0], segments)
        elif cmd == "pyAudioAnalysis":
            segments = diarize_pa(audio_path)
            print(segments)
        else:
            print("Invalid segmentation method!")
        