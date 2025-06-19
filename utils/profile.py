import os
import yaml
import json

def load_profile(profile_path):
    if not os.path.isfile(profile_path):
        raise FileNotFoundError(f"Профиль {profile_path} не найден")
    if profile_path.endswith((".yaml", ".yml")):
        with open(profile_path, "r") as f:
            return yaml.safe_load(f)
    elif profile_path.endswith(".json"):
        with open(profile_path, "r") as f:
            return json.load(f)
    else:
        raise ValueError("Поддерживаются только .yaml, .yml, .json профили")