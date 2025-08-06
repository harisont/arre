import os
import sys
import argparse
import torch
import stable_whisper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe with stable-ts (Whisper)")
    parser.add_argument("audio", help="path to the audio file")
    parser.add_argument(
        "-p", "--prompt", 
        help="path to the prompt",
        default="Mongiovì Angelo, difeso dagli avvocati Grillo e Mongiovì.")
    parser.add_argument(
        "-l", "--lang", 
        help="two-letter ISO language code, e.g. 'it' for Italian", 
        default="it"
    )
    parser.add_argument(
        "-t", "--vad-threshold", 
        help="Voice Activity Detection threshold (a float between 0 and 1)", 
        type=float,
        default=0.4
    )
    args = parser.parse_args()
    audio_path = args.audio
    prompt_path = args.prompt
    lang = args.lang
    threshold = args.vad_threshold
    params = {
        "device": "cuda:0" if torch.cuda.is_available() else "cpu"
    }
    model = stable_whisper.load_model("medium", **params)
    with open(prompt_path) as f:
        prompt = f.read()
    opts = {"language": lang}
    result = model.transcribe(audio_path, initial_prompt=prompt, vad_threshold=threshold, **opts)
    result.to_srt_vtt(os.path.splitext(audio_path)[0] + ".srt")
