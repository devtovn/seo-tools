import os
from playwright.async_api import async_playwright
from playwright_bot.stealth import apply_stealth
from config import HEADLESS


async def create_browser(profile_info, p=None):
    """
    Tạo browser với geolocation theo tỉnh thành
    Args:
        profile_info: dict với keys "path" và "province" 
                      hoặc string (backward compatible)
        p: Playwright instance (optional)
    """
    # Xử lý backward compatibility
    if isinstance(profile_info, str):
        profile_path = profile_info
        province = None
    else:
        profile_path = profile_info["path"]
        province = profile_info["province"]
    
    started = False
    if p is None:
        p = await async_playwright().start()
        started = True

    # Cấu hình geolocation nếu có province info
    context_options = {
        "user_data_dir": profile_path,
        "headless": HEADLESS,
        "args": ["--disable-blink-features=AutomationControlled"]
    }
    
    if province:
        # Set geolocation và permissions
        context_options["geolocation"] = {
            "latitude": province["latitude"],
            "longitude": province["longitude"]
        }
        context_options["permissions"] = ["geolocation"]
        
        print(f"[GEOLOCATION] Profile: {os.path.basename(profile_path)} -> {province['name']} "
              f"({province['latitude']}, {province['longitude']})")

    context = await p.chromium.launch_persistent_context(**context_options)

    await apply_stealth(context)
    return p, context
