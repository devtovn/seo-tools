import asyncio
import random
from common.page_detector import detect_google_block
from config import (
    MIN_KEY_DELAY,
    MAX_KEY_DELAY,
    SCROLL_SLEEP_MIN,
    SCROLL_SLEEP_MAX,
    PAGE_NAV_MIN,
    PAGE_NAV_MAX,
    DETAIL_SCROLL_DOWN_S,
    DETAIL_SCROLL_DOWN_SPEED_FACTOR,
    DETAIL_READ_S,
    DETAIL_SCROLL_UP_S,
)

 
async def google_search(page, keyword, target_domain="hanabeautybox.vn", max_pages=5):
    await page.goto("https://www.google.com", wait_until="domcontentloaded")

    status = await detect_google_block(page)
    if status != "OK":
        raise RuntimeError(f"Google blocked: {status}")

    await page.wait_for_selector("textarea[name='q']", timeout=60000)

    box = page.locator("textarea[name='q']")
    await box.focus()

    for ch in keyword:
        await page.keyboard.type(ch)
        await asyncio.sleep(random.uniform(MIN_KEY_DELAY, MAX_KEY_DELAY))

    await page.keyboard.press("Enter")
    await asyncio.sleep(random.uniform(PAGE_NAV_MIN, PAGE_NAV_MAX))

    # After search: try to find and click the target domain in results.
    for _ in range(max_pages):
        selector = f"a[href*='{target_domain}']"
        handles = await page.locator(selector).element_handles()
        if handles:
            try:
                await handles[0].click()
                await page.wait_for_load_state('domcontentloaded')

                # On the target site: find `input[name="query"]`, type cleaned keyword,
                # submit and keep the page for 60s via wait_for_selector timeout.
                try:
                    # cleaned keyword: remove phrase "hana beauty box" (case-insensitive)
                    cleaned = keyword.replace("hana beauty box", "")
                    cleaned = cleaned.replace("Hana Beauty Box", "")
                    cleaned = cleaned.strip()
                    if not cleaned:
                        cleaned = keyword

                    await page.wait_for_selector("input[name='query']", timeout=50000)
                    q = page.locator("input[name='query']")
                    await q.focus()
                    for ch in cleaned:
                        await page.keyboard.type(ch)
                        await asyncio.sleep(random.uniform(MIN_KEY_DELAY, MAX_KEY_DELAY))

                    await page.keyboard.press('Enter')

                    # wait for results to load (up to 60s)
                    try:
                        await page.wait_for_selector("a[title]", timeout=60000)
                    except Exception:
                        # no result links found within timeout
                        return

                    # find first anchor whose title contains the cleaned keyword (case-insensitive)
                    handles = await page.locator("a[title]").element_handles()
                    target_lower = cleaned.lower()
                    clicked = False
                    for h in handles:
                        try:
                            title = (await h.get_attribute('title')) or ''
                            if target_lower in title.lower():
                                try:
                                    await h.click()
                                    await page.wait_for_load_state('domcontentloaded')

                                    # on the detail page: perform a slow scroll down (time-based),
                                    # pause to read, then a (faster) slow scroll up. Durations are
                                    # configured in `config.py` (DETAIL_SCROLL_DOWN_S, DETAIL_READ_S,
                                    # DETAIL_SCROLL_UP_S, DETAIL_SCROLL_UP_SPEED_FACTOR).

                                    tick = 0.5
                                    loop = asyncio.get_event_loop()

                                    # slow scroll down: try to reach bottom in DETAIL_SCROLL_DOWN_S seconds
                                    start = loop.time()
                                    end = start + float(DETAIL_SCROLL_DOWN_S)
                                    while loop.time() < end:
                                        now = loop.time()
                                        remaining_ticks = max(1, int((end - now) / tick))
                                        # remaining height to bottom
                                        rem_height = await page.evaluate("document.body.scrollHeight - window.scrollY")
                                        per_scroll = rem_height / remaining_ticks
                                        if per_scroll <= 0:
                                            break
                                        await page.evaluate(f"window.scrollBy(0, {per_scroll})")
                                        await asyncio.sleep(min(tick, end - now))

                                    # ensure at bottom
                                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                                    # New sequence per request:
                                    # 1) small scroll up from bottom, wait 1s
                                    await page.evaluate("window.scrollBy(0, -window.innerHeight)")
                                    await asyncio.sleep(1)

                                    # 2) scroll up to middle of the page and wait (DETAIL_READ_S)
                                    mid = await page.evaluate("document.body.scrollHeight / 2")
                                    await page.evaluate(f"window.scrollTo(0, {mid})")
                                    await asyncio.sleep(DETAIL_READ_S)

                                    # 3) scroll down in 7 steps from middle (split remaining distance into 7)
                                    steps_down = 7
                                    for _ in range(steps_down):
                                        rem = await page.evaluate("document.body.scrollHeight - window.scrollY")
                                        per = rem / max(1, steps_down)
                                        if per <= 0:
                                            break
                                        await page.evaluate(f"window.scrollBy(0, {per})")
                                        await asyncio.sleep(0.5)

                                    # 4) fast scroll up to top within configured up duration & speed factor
                                    up_total = float(DETAIL_SCROLL_UP_S) * float(DETAIL_SCROLL_DOWN_SPEED_FACTOR)
                                    up_tick = 0.1
                                    up_loop = asyncio.get_event_loop()
                                    up_start = up_loop.time()
                                    up_end = up_start + up_total
                                    while up_loop.time() < up_end:
                                        now = up_loop.time()
                                        remaining_ticks = max(1, int((up_end - now) / up_tick))
                                        rem_up = await page.evaluate("window.scrollY")
                                        per_up = rem_up / remaining_ticks
                                        if per_up <= 0:
                                            break
                                        await page.evaluate(f"window.scrollBy(0, -{per_up})")
                                        await asyncio.sleep(min(up_tick, up_end - now))

                                    # ensure at top
                                    await page.evaluate("window.scrollTo(0, 0)")

                                    clicked = True
                                    break
                                except Exception:
                                    continue
                        except Exception:
                            continue

                    if not clicked:
                        # fallback: try clicking any visible link with href
                        for h in handles:
                            try:
                                href = await h.get_attribute('href')
                                if href:
                                    await h.click()
                                    await page.wait_for_load_state('domcontentloaded')
                                    clicked = True
                                    break
                            except Exception:
                                continue

                    return
                except Exception:
                    # If target input not found or typing fails, still return to caller
                    return
            except Exception:
                pass

        # not found on this view: try scrolling to load more results
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(random.uniform(SCROLL_SLEEP_MIN, SCROLL_SLEEP_MAX))

        # If there's a next page button, click it to go to next results page
        next_count = await page.locator("a#pnnext").count()
        if next_count:
            try:
                await page.locator("a#pnnext").first.click()
                await asyncio.sleep(random.uniform(PAGE_NAV_MIN, PAGE_NAV_MAX))
                continue
            except Exception:
                break

    raise RuntimeError(f"Target domain not found in search results: {target_domain}")
