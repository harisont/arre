import os
import sys
import stable_whisper

if __name__ == "__main__":
    audio_path = sys.argv[1]
    model = stable_whisper.load_model('base')
    with open("asr_prompt.txt") as f:
        prompt = f.read()
    result = model.transcribe(audio_path, initial_prompt=prompt)
    result.to_srt_vtt(os.path.splitext(audio_path)[0] + ".srt")