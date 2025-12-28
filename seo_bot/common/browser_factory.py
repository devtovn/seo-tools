import undetected_chromedriver as uc
from common.stealth import apply_stealth
from common.profile_manager import get_next_profile
from config import HEADLESS

def create_browser(profile_path=None):
    if profile_path is None:
        profile_path = get_next_profile()

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = uc.Chrome(
        options=options,
        headless=HEADLESS,
        use_subprocess=True
    )

    apply_stealth(driver)
    return driver
