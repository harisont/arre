from os import path
import sys
from pydub import AudioSegment
  
def mp3_to_wav(file_path):
    sound = AudioSegment.from_mp3(file_path)
    sound.export(path.splitext(file_path)[0] + ".wav", format="wav")
    
if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        mp3_to_wav(file_path)