from selenium.webdriver.common.by import By
from common.human_actions import human_typing, human_delay
import time
import random
from config import SCROLL_SLEEP_MIN, SCROLL_SLEEP_MAX, PAGE_NAV_MIN, PAGE_NAV_MAX

class GoogleSearchService:

    def __init__(self, driver):
        self.driver = driver

    def open_google(self):
        self.driver.get("https://www.google.com")

    def search(self, keyword):
        box = self.driver.find_element(By.NAME, "q")
        box.clear()
        human_typing(box, keyword)
        box.submit()
        human_delay()

        # After submitting, try to find and click the target domain in results.
        target = "hanabeautybox.vn"
        max_pages = 5
        for _ in range(max_pages):
            links = self.driver.find_elements(By.CSS_SELECTOR, f"a[href*='{target}']")
            if links:
                try:
                    links[0].click()
                    return
                except Exception:
                    pass

            # scroll and wait for more results to load
            self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(random.uniform(SCROLL_SLEEP_MIN, SCROLL_SLEEP_MAX))

            # try to click Next page if present
            try:
                nxt = self.driver.find_element(By.ID, "pnnext")
                if nxt:
                    nxt.click()
                    time.sleep(random.uniform(PAGE_NAV_MIN, PAGE_NAV_MAX))
                    continue
            except Exception:
                break
