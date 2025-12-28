import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# BROWSER
# =========================
HEADLESS = False

# =========================
# PLAYWRIGHT
# =========================
# (Playwright args are set inline in playwright_bot/browser.py)
# Playwright args are set inline where the browser/context is created.

# =========================
# ASYNC HUMAN BEHAVIOR
# =========================
MIN_KEY_DELAY = 0.01
MAX_KEY_DELAY = 0.08

# per-session limits are not enforced centrally in code; remove if unused.

# Human delay defaults used by sync helpers
HUMAN_DELAY_MIN_S = 1
HUMAN_DELAY_MAX_S = 2

# Short scroll wait (used when scrolling to load more results)
SCROLL_SLEEP_MIN = 3
SCROLL_SLEEP_MAX = 5

# Page navigation / small action waits (used for clicking next, waiting for navigation)
PAGE_NAV_MIN = 1
PAGE_NAV_MAX = 2

# Detail page interaction timings
# Slow scroll down duration (seconds)
DETAIL_SCROLL_DOWN_S = 5 #45
# Factor applied to per-step sleep when scrolling down; <1 makes scroll-down faster
DETAIL_SCROLL_DOWN_SPEED_FACTOR = 0.3
# Pause to simulate reading (seconds)
DETAIL_READ_S = 3 #10
# Slow scroll up duration (seconds)
DETAIL_SCROLL_UP_S =  5 #10
# Number of steps to split the slow scroll into
DETAIL_SCROLL_STEPS = 5 #50
# Factor applied to per-step sleep when scrolling up; <1 makes scroll-up faster
DETAIL_SCROLL_UP_SPEED_FACTOR = 0.1

# =========================
# BLOCK DETECTION
# =========================
# Detection logic lives in `common/page_detector.py` (simple title/url checks).

# =========================
# IO
# =========================
RESULT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULT_DIR, exist_ok=True)
