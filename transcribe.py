import os
import sys
import stable_whisper

if __name__ == "__main__":
    audio_path = sys.argv[1]
    model = stable_whisper.load_model('small')
    with open("whisper_prompt.txt") as f:
        prompt = f.read()
        print(prompt)
    result = model.transcribe(audio_path, initial_prompt=prompt, vad_threshold=0.45)
    result.to_srt_vtt(os.path.splitext(audio_path)[0] + ".srt")