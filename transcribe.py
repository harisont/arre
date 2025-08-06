import os
import sys
import torch
import stable_whisper

if __name__ == "__main__":
    audio_path = sys.argv[1]
    prompt_path = sys.argv[2]
    params = {
        "device": "cuda:0" if torch.cuda.is_available() else "cpu"
    }
    model = stable_whisper.load_model("medium", **params)
    with open(prompt_path) as f:
        prompt = f.read()
        print(prompt)
    opts = {"language": "it"}
    result = model.transcribe(audio_path, initial_prompt=prompt, vad_threshold=0.45, **opts)
    result.to_srt_vtt(os.path.splitext(audio_path)[0] + ".srt")
