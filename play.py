import pyaudio
import wave

def play_segment(audio_path, start,stop):
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
