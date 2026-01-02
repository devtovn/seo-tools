import asyncio
import os
from playwright_bot.browser import create_browser
from playwright_bot.google_search_async import google_search
from common.profile_manager import get_random_profile_for_keyword, delete_profile


def load_keywords(isRandom: bool = False, path: str = "keywords.txt"):
    with open(path, encoding="utf-8") as f:
        kws = [k.strip() for k in f if k.strip()]
    if not kws:
        return []
    if isRandom:
        import random
        return [random.choice(kws)]
    return kws

async def main():
    playwright_p = None
    try:
        while True:
            keywords = load_keywords(isRandom=False)
            if not keywords:
                await asyncio.sleep(1)
                continue

            for kw in keywords:
                # Random chọn 1 profile cho mỗi keyword
                profile_info = get_random_profile_for_keyword(kw)
                print(f"[KEYWORD] {kw} -> Profile: {os.path.basename(profile_info['path'])} "
                      f"-> Tỉnh: {profile_info['province']['name']}")
                
                playwright_p, context = await create_browser(profile_info, playwright_p)
                page = await context.new_page()

                try:
                    await google_search(page, kw + " hana beauty box")
                except Exception as e:
                    print(f"[SKIP] {kw} - {e}")
                finally:
                    try:
                        await context.close()
                    except Exception:
                        pass
                    
                    # Xóa profile sau khi chạy xong keyword
                    delete_profile(profile_info['path'])

            await asyncio.sleep(1)
    finally:
        if playwright_p is not None:
            try:
                await playwright_p.stop()
            except Exception:
                pass

asyncio.run(main())
