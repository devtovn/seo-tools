import random
import json

async def apply_stealth(context):
    choices = [
        ["en-US", "en"],
        ["vi-VN", "vi"],
        ["en-GB", "en"],
        ["en-US", "en", "vi"],
        ["vi-VN", "vi", "en-US"],
    ]
    langs = random.choice(choices)
    langs_js = json.dumps(langs)
    await context.add_init_script(f"""
        Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});
        Object.defineProperty(navigator, 'languages', {{ get: () => {langs_js} }});
        Object.defineProperty(navigator, 'platform', {{ get: () => 'Win32' }});
    """)
        