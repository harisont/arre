import os
import sys
import pyaudio
import wave
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# import vlc

def play_segment(audio_path, start, stop):
    wav = wave.open(audio_path, 'rb')
    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(
            format=py_audio.get_format_from_width(wav.getsampwidth()),
            channels=wav.getnchannels(),
            rate=wav.getframerate(),
            output=True
        )
    skipped_frames = int(start * wav.getframerate())
    wav.setpos(skipped_frames)
    n_frames = int((stop - start) * wav.getframerate())
    frames = wav.readframes(n_frames)
    stream.write(frames)
    stream.close()
    py_audio.terminate()
    wav.close()

def play_segment_vlc(audio_path, start, stop):
    segment_path = os.path.join(os.path.dirname(audio_path), 'tmp.wav')
    ffmpeg_extract_subclip(audio_path, start, stop, segment_path)
    # TODO: separate Windows command
    os.system("nohup vlc --loop " + segment_path + " &") 

    # tried using vlc lib but did not manage to launch with UI. Same with MPV
    '''
    media_player = vlc.MediaPlayer()
    # media = vlc.Media(audio_path)
    # media_player.set_media(media)
    # media_player.play()
    '''

if __name__ == "__main__":
    audio_path = sys.argv[1]
    start = float(sys.argv[2])
    stop = float(sys.argv[3])
    play_segment(audio_path, start, stop)