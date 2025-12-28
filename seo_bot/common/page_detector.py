async def detect_google_block(page):
    url = page.url

    if "sorry" in url:
        return "CAPTCHA"

    title = await page.title()
    if "unusual traffic" in title.lower():
        return "BLOCKED"

    return "OK"
