import sys
import csv
from os import path
from itertools import groupby
from pyannote.audio import Pipeline
from inaSpeechSegmenter import Segmenter

# Diarization with pyannote-audio (too slow to be useful)

'''Given its path, diarize a .wav file, returning a list of audio segments,
   audio_path needs to point to a .wav file
'''
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

'''Basic speech/noEnergy/noise/music segmentation via inaSpeechSegmenter'''
def segment_ina(audio_path):
    segmenter = Segmenter(detect_gender=False)
    return segmenter(audio_path)

'''Rule-based refinement of segments obtained via inaSpeechSegmenter.
   - noEnergy/noise/music -> pause (simplify_labels)
   - rm pauses shorter than max sec (rm_short_pauses)
   - merge contiguous same-label segments (merge_contiguous)
'''
def refine_ina(segments):
    def simplify_labels(segments):
        return list(map(
            lambda s: (s[0] if s[0] == "speech" else "pause",s[1],s[2]), 
            segments
            ))
    def rm_short_pauses(segments, max=2):
        return list(filter(
            lambda s: 
                s[0] == "speech" or (s[0] == "pause" and s[2] - s[1] >= max),
            segments
            ))
    def merge_contiguous(segments):
        groups = list(map(
            lambda g: list(g[1]), 
            groupby(segments, lambda s: s[0])
            ))
        return list(map(lambda g: (g[0][0], g[0][1], g[-1][2]), groups))
    return merge_contiguous(rm_short_pauses(simplify_labels(segments)))


if __name__ == "__main__":
    cmd = sys.argv[1]
    for audio_path in sys.argv[2:]:
        if cmd == "diarize":
            segments = diarize_pa(audio_path)
            segments_to_csv_pa(path.splitext(audio_path)[0], segments)
        elif cmd == "simple-segment":
            segments = refine_ina(segment_ina(audio_path))
            segments_to_csv_pa(path.splitext(audio_path)[0], segments)
        else:
            print("Invalid segmentation method!")
        