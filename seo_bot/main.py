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
    BREAK_DURATION_MIN, BREAK_DURATION_MAX,
    FIRST_START_MAX_HOUR, STARTUP_DELAY_SECONDS
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


def get_random_start_time(is_first_of_day=False):
    """Generate a random start time
    If is_first_of_day=True: time will be between START_TIME_HOUR_MIN and FIRST_START_MAX_HOUR
    Otherwise: between START_TIME_HOUR_MIN and START_TIME_HOUR_MAX
    """
    if is_first_of_day:
        # First start of the day: must be before FIRST_START_MAX_HOUR
        max_hour = FIRST_START_MAX_HOUR - 1  # e.g., if FIRST_START_MAX_HOUR=7, max_hour=6
        hour = random.randint(START_TIME_HOUR_MIN, max_hour)
        if hour == max_hour:
            minute = random.randint(START_TIME_MINUTE_MIN, 59)
        else:
            minute = random.randint(START_TIME_MINUTE_MIN, START_TIME_MINUTE_MAX)
    else:
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
    last_start_datetime = None
    current_date = None
    is_first_startup = True
    try:
        while True:
            now = datetime.now()
            
            # First startup: run after STARTUP_DELAY_SECONDS
            if is_first_startup:
                print(f"[TIMING] First startup, will run after {STARTUP_DELAY_SECONDS} seconds...")
                await asyncio.sleep(STARTUP_DELAY_SECONDS)
                is_first_startup = False
                current_date = now.date()
                last_start_datetime = datetime.now()
            # Check if it's a new day
            elif current_date is None or current_date != now.date():
                # First run of the day: schedule before FIRST_START_MAX_HOUR
                current_date = now.date()
                start_time = get_random_start_time(is_first_of_day=True)
                target_datetime = datetime.combine(now.date(), start_time)
                
                # If already past FIRST_START_MAX_HOUR today, schedule for tomorrow
                if now.time() >= time(FIRST_START_MAX_HOUR, 0):
                    target_datetime += timedelta(days=1)
                    current_date = target_datetime.date()
                
                print(f"[TIMING] First run of the day, waiting until {target_datetime.strftime('%Y-%m-%d %H:%M')}...")
                await wait_until_start_time(start_time if now.date() == target_datetime.date() else start_time)
                last_start_datetime = target_datetime
            else:
                # Subsequent runs: must be after previous start + break duration
                break_minutes = random.randint(BREAK_DURATION_MIN, BREAK_DURATION_MAX)
                next_start_datetime = last_start_datetime + timedelta(minutes=break_minutes)
                
                # If next start is on a different day, reset to first of day logic
                if next_start_datetime.date() != current_date:
                    current_date = next_start_datetime.date()
                    start_time = get_random_start_time(is_first_of_day=True)
                    next_start_datetime = datetime.combine(next_start_datetime.date(), start_time)
                
                wait_seconds = (next_start_datetime - datetime.now()).total_seconds()
                if wait_seconds > 0:
                    print(f"[TIMING] Next run scheduled at {next_start_datetime.strftime('%Y-%m-%d %H:%M')} (after {break_minutes} min break)...")
                    await asyncio.sleep(wait_seconds)
                
                last_start_datetime = next_start_datetime
            
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
