import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def scrape_reviews(maps_url, status_callback=None):
    options = Options()
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        if status_callback:
            status_callback("Opening Google Maps page...")

        driver.get(maps_url)
        time.sleep(5)

        try:
            accept_btn = driver.find_element(By.XPATH, '//button[normalize-space()="Accept all"]')
            accept_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

        if status_callback:
            status_callback("🔎 Looking for 'Reviews' tab...")

        tab_buttons = driver.find_elements(By.TAG_NAME, "button")
        for tab in tab_buttons:
            if "review" in tab.text.strip().lower():
                tab.click()
                time.sleep(4)
                break

        try:
            scrollable_div = driver.find_element(By.XPATH, '//div[contains(@class, "m6QErb DxyBCb kA9KIf dS8AEf")]')
        except NoSuchElementException:
            if status_callback:
                status_callback("Could not find scrollable review container.")
            return None

        if status_callback:
            status_callback("⬇️ Scrolling to load all reviews...")

        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        scroll_attempts = 0
        max_scroll_attempts = 30

        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2.0)

            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height

        if status_callback:
            status_callback("Done scrolling. Extracting reviews...")

        reviews = driver.find_elements(By.XPATH, '//div[contains(@class, "jftiEf")]')
        data = []

        for review in reviews:
            try:
                author = review.find_element(By.CLASS_NAME, 'd4r55').text
                stars_element = review.find_element(By.CLASS_NAME, 'kvMYJc')
                stars = stars_element.get_attribute('aria-label')
                rating = int(stars[0]) if stars else None
                time_posted = review.find_element(By.CLASS_NAME, 'rsqaWe').text
                text = review.find_element(By.CLASS_NAME, 'wiI7pd').text
                data.append([author, rating, time_posted, text])
            except Exception:
                continue

        if status_callback:
            status_callback(f"📦 Total reviews extracted: {len(data)}")

        df = pd.DataFrame(data, columns=["Author", "Rating", "Posted", "Review"])
        output_file = "reviews.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        return output_file

    except Exception as e:
        if status_callback:
            status_callback(f"Error: {e}")
        return None
    finally:
        driver.quit()
   