import asyncio
import os
import random
from datetime import datetime, time, timedelta
from playwright_bot.browser import create_browser
from playwright_bot.google_search_async import google_search
from common.profile_manager import get_random_profile_for_keyword, delete_profile
from config import (
    START_TIME_HOUR_MIN, START_TIME_HOUR_MAX,
    START_TIME_MINUTE_MIN, START_TIME_MINUTE_MAX,
    KEYWORDS_BEFORE_BREAK_MIN, KEYWORDS_BEFORE_BREAK_MAX,
    BREAK_DURATION_MIN, BREAK_DURATION_MAX
)


def load_keywords(isRandom: bool = False, path: str = "keywords.txt"):
    with open(path, encoding="utf-8") as f:
        kws = [k.strip() for k in f if k.strip()]
    if not kws:
        return []
    if isRandom:
        import random
        return [random.choice(kws)]
    return kws


def get_random_start_time():
    """Generate a random start time between 6:xx AM and 22:yy PM"""
    hour = random.randint(START_TIME_HOUR_MIN, START_TIME_HOUR_MAX)
    minute = random.randint(START_TIME_MINUTE_MIN, START_TIME_MINUTE_MAX)
    return time(hour, minute)


def get_random_break_settings():
    """Get random number of keywords before break and break duration"""
    keywords_count = random.randint(KEYWORDS_BEFORE_BREAK_MIN, KEYWORDS_BEFORE_BREAK_MAX)
    break_minutes = random.randint(BREAK_DURATION_MIN, BREAK_DURATION_MAX)
    return keywords_count, break_minutes


async def wait_until_start_time(target_time):
    """Wait until the target start time"""
    now = datetime.now()
    target_datetime = datetime.combine(now.date(), target_time)
    
    # If target time is already passed today, schedule for tomorrow
    if target_datetime < now:
        target_datetime += timedelta(days=1)
    
    wait_seconds = (target_datetime - now).total_seconds()
    if wait_seconds > 0:
        print(f"[TIMING] Waiting until {target_datetime.strftime('%Y-%m-%d %H:%M')} to start searching...")
        await asyncio.sleep(wait_seconds)


async def main():
    playwright_p = None
    is_first_run = True
    try:
        while True:
            # Skip waiting on first run, wait for random start time on subsequent runs
            if is_first_run:
                print("[TIMING] Starting immediately on first run...")
                is_first_run = False
            else:
                start_time = get_random_start_time()
                await wait_until_start_time(start_time)
            
            # Get random break settings
            keywords_before_break, break_duration = get_random_break_settings()
            print(f"[TIMING] Will search {keywords_before_break} keywords, then break for {break_duration} minutes")
            
            keywords = load_keywords(isRandom=False)
            if not keywords:
                await asyncio.sleep(1)
                continue

            keyword_count = 0
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
                
                keyword_count += 1
                
                # Check if it's time for a break
                if keyword_count >= keywords_before_break:
                    print(f"[BREAK] Completed {keyword_count} keywords. Taking a break for {break_duration} minutes...")
                    await asyncio.sleep(break_duration * 60)
                    
                    # Reset counter and get new random break settings
                    keyword_count = 0
                    keywords_before_break, break_duration = get_random_break_settings()
                    print(f"[TIMING] Next cycle: will search {keywords_before_break} keywords, then break for {break_duration} minutes")

            await asyncio.sleep(1)
    finally:
        if playwright_p is not None:
            try:
                await playwright_p.stop()
            except Exception:
                pass


asyncio.run(main())
