import os
import sys
import torch
import stable_whisper

if __name__ == "__main__":
    audio_path = sys.argv[1]
    params = {
        "device": "cuda:0" if torch.cuda.is_available() else "cpu",
        "compute_type": "float32"
    }
    model = stable_whisper.load_model("medium", **params)
    with open("whisper_prompt.txt") as f:
        prompt = f.read()
        print(prompt)
    opts = {"language": "it"}
    result = model.transcribe(audio_path, initial_prompt=prompt, vad_threshold=0.45, **opts)
    result.to_srt_vtt(os.path.splitext(audio_path)[0] + ".srt")