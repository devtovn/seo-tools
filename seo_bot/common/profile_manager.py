import os
import itertools
import random
import json

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
BASE_PROFILE_DIR = os.path.join(BASE_DIR, "seo_profiles")
MAPPING_FILE = os.path.join(BASE_DIR, "profile_map.json")

_profiles = [
    os.path.join(BASE_PROFILE_DIR, f"profile_{i}")
    for i in range(1, 10)
]

_profile_cycle = itertools.cycle(_profiles)


def _load_map():
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def _save_map(mapping):
    with open(MAPPING_FILE, "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, ensure_ascii=False, indent=2)


def get_profile_for_keyword(keyword: str) -> str:
    mapping = _load_map()
    if keyword in mapping and os.path.exists(mapping[keyword]):
        return mapping[keyword]

    existing = [p for p in _profiles if os.path.exists(p)]
    if existing:
        profile = random.choice(existing)
    else:
        profile = random.choice(_profiles)
        os.makedirs(profile, exist_ok=True)

    mapping[keyword] = profile
    _save_map(mapping)
    return profile


def get_next_profile():
    profile = next(_profile_cycle)
    os.makedirs(profile, exist_ok=True)
    return profile
