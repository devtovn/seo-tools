import os
import itertools
import random
import json
import sys
import shutil

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
sys.path.insert(0, BASE_DIR)

from province_config import get_province_by_profile_number

BASE_PROFILE_DIR = os.path.join(BASE_DIR, "seo_profiles")
MAPPING_FILE = os.path.join(BASE_DIR, "profile_map.json")

# Tạo 63 profiles tương ứng với 63 tỉnh thành Việt Nam
_profiles = [
    os.path.join(BASE_PROFILE_DIR, f"profile_{i}")
    for i in range(1, 64)  # 63 profiles
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


def get_profile_for_keyword(keyword: str) -> dict:
    """
    Trả về dictionary chứa profile path và province info
    """
    mapping = _load_map()
    if keyword in mapping and os.path.exists(mapping[keyword]):
        profile_path = mapping[keyword]
    else:
        existing = [p for p in _profiles if os.path.exists(p)]
        if existing:
            profile_path = random.choice(existing)
        else:
            profile_path = random.choice(_profiles)
            os.makedirs(profile_path, exist_ok=True)

        mapping[keyword] = profile_path
        _save_map(mapping)
    
    # Lấy profile number từ path (ví dụ: profile_5 -> 5)
    profile_number = int(os.path.basename(profile_path).split('_')[1])
    province_info = get_province_by_profile_number(profile_number)
    
    return {
        "path": profile_path,
        "province": province_info
    }


def get_next_profile():
    """
    Trả về dictionary chứa profile path và province info
    """
    profile_path = next(_profile_cycle)
    os.makedirs(profile_path, exist_ok=True)
    
    # Lấy profile number từ path
    profile_number = int(os.path.basename(profile_path).split('_')[1])
    province_info = get_province_by_profile_number(profile_number)
    
    return {
        "path": profile_path,
        "province": province_info
    }


def get_random_profile_for_keyword(keyword: str) -> dict:
    """
    Random chọn 1 profile ngẫu nhiên cho keyword (không lưu vào mapping).
    Mỗi lần gọi sẽ tạo profile mới với số ngẫu nhiên từ 1-63.
    Trả về dictionary chứa profile path và province info.
    """
    # Random chọn profile number từ 1-63
    profile_number = random.randint(1, 63)
    profile_path = os.path.join(BASE_PROFILE_DIR, f"profile_{profile_number}")
    
    # Tạo profile directory nếu chưa tồn tại
    os.makedirs(profile_path, exist_ok=True)
    
    # Lấy thông tin tỉnh thành
    province_info = get_province_by_profile_number(profile_number)
    
    return {
        "path": profile_path,
        "province": province_info
    }


def delete_profile(profile_path: str):
    """
    Xóa profile directory và cập nhật mapping file nếu cần.
    """
    try:
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)
            print(f"[DELETED] Profile: {os.path.basename(profile_path)}")
        
        # Xóa profile khỏi mapping file nếu có
        mapping = _load_map()
        keys_to_remove = [k for k, v in mapping.items() if v == profile_path]
        for key in keys_to_remove:
            del mapping[key]
        
        if keys_to_remove:
            _save_map(mapping)
    except Exception as e:
        print(f"[ERROR] Failed to delete profile: {e}")
