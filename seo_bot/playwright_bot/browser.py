from playwright.async_api import async_playwright
from playwright_bot.stealth import apply_stealth
from config import HEADLESS


async def create_browser(profile_path, p=None):
    started = False
    if p is None:
        p = await async_playwright().start()
        started = True

    context = await p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=HEADLESS,
        args=["--disable-blink-features=AutomationControlled"]
    )

    await apply_stealth(context)
    return p, context
