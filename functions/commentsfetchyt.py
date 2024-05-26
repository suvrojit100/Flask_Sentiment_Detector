import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

def scrapfyt(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--mute-audio')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_window_size(960, 800)
    time.sleep(1)
    driver.get(url)
    time.sleep(2)

    usernames, comments = [], []

    try:
        pause = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))
        pause.click()
        time.sleep(0.2)
        pause.click()
        time.sleep(4)

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(4)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
        comments_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

        for username, comment in zip(users, comments_elements):
            usernames.append(username.text)
            comments.append(comment.text)

    except exceptions.TimeoutException:
        print("Timeout occurred while scraping comments.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    df = pd.DataFrame({'Username': usernames, 'Comment': comments})
    return df

# Example usage
url = 'https://www.youtube.com/watch?v=b3Kv_TeG07I'
df = scrapfyt(url)
print(df.head())

