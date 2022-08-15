import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

AUDIO_PLAYER_CMD = config["audio_player_cmd"]
TXT_EDITOR_CMD = config["text_editor_cmd"]