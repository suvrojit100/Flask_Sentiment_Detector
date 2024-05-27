import os
import time
import io
import pandas as pd
import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager
from langdetect import detect
from googletrans import Translator

def scrapfyt(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--mute-audio')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--log-level=3')  # Suppress warnings and errors

    # Initialize the driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.set_window_size(960, 800)
    time.sleep(1)
    driver.get(url)
    time.sleep(2)

    try:
        # Pause YouTube video
        pause = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))
        pause.click()
        time.sleep(0.2)
        pause.click()
        time.sleep(4)

        # Scrolling through all the comments
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(4)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Scraping details
        video_title = driver.find_element(By.NAME, 'title').get_attribute('content')
        video_owner1 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
        video_owner = video_owner1[0].text if video_owner1 else 'Unknown'
        video_comment_with_replies = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text + ' Comments'
        users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
        comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

        csv_file_path = 'comments.csv'
        with io.open(csv_file_path, 'w', newline='', encoding="utf-16") as file:
            writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
            writer.writerow(["Username", "Comment"])
            for username, comment in zip(users, comments):
                writer.writerow([username.text, comment.text])

    except exceptions.TimeoutException:
        print("Timeout occurred while scraping comments.")
        csv_file_path = ''
    except Exception as e:
        print(f"An error occurred: {e}")
        csv_file_path = ''
    finally:
        driver.quit()

    return translate_comments(csv_file_path)

def translate_comments(csv_file_path):
    translator = Translator()
    commentsfile = pd.read_csv(csv_file_path, encoding="utf-16")
    
    translated_comments = []
    for index, row in commentsfile.iterrows():
        username = row['Username']
        comment = row['Comment']
        try:
            if pd.isna(comment) or not isinstance(comment, str) or comment.strip() == "":
                continue
            lang = detect(comment)
            if lang != 'en':
                translated_comment = translator.translate(comment, dest='en').text
                translated_comments.append([username, translated_comment])
            else:
                translated_comments.append([username, comment])
        except Exception as e:
            print(f"An error occurred during translation: {e}")

    df = pd.DataFrame(translated_comments, columns=["Username", "Comment"])
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    new_csv_file_path = 'translated_comments.csv'
    df.to_csv(new_csv_file_path, index=False, encoding="utf-16")

    return df


# import os
# import time
# import io
# import pandas as pd
# import numpy as np
# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common import exceptions
# from webdriver_manager.chrome import ChromeDriverManager
# from langdetect import detect
# from googletrans import Translator

# def scrapfyt(url):
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--mute-audio')
#     options.add_argument('--disable-extensions')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--disable-gpu')  # Disable GPU acceleration
#     options.add_argument('--log-level=3')  # Suppress warnings and errors

#     # Initialize the driver
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

#     driver.set_window_size(960, 800)
#     time.sleep(1)
#     driver.get(url)
#     time.sleep(2)

#     try:
#         # Pause YouTube video
#         pause = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))
#         pause.click()
#         time.sleep(0.2)
#         pause.click()
#         time.sleep(4)

#         # Scrolling through all the comments
#         last_height = driver.execute_script("return document.documentElement.scrollHeight")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#             time.sleep(4)
#             new_height = driver.execute_script("return document.documentElement.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         # Scraping details
#         video_title = driver.find_element(By.NAME, 'title').get_attribute('content')
#         video_owner1 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
#         video_owner = video_owner1[0].text if video_owner1 else 'Unknown'
#         video_comment_with_replies = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text + ' Comments'
#         users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
#         comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

#         csv_file_path = 'comments.csv'
#         with io.open(csv_file_path, 'w', newline='', encoding="utf-16") as file:
#             writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
#             writer.writerow(["Username", "Comment"])
#             for username, comment in zip(users, comments):
#                 writer.writerow([username.text, comment.text])

#     except exceptions.TimeoutException:
#         print("Timeout occurred while scraping comments.")
#         csv_file_path = ''
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         csv_file_path = ''
#     finally:
#         driver.quit()

#     return translate_comments(csv_file_path)

# def translate_comments(csv_file_path):
#     translator = Translator()
#     commentsfile = pd.read_csv(csv_file_path, encoding="utf-16")
    
#     translated_comments = []
#     for index, row in commentsfile.iterrows():
#         username = row['Username']
#         comment = row['Comment']
#         try:
#             if pd.isna(comment) or not isinstance(comment, str) or comment.strip() == "":
#                 continue
#             lang = detect(comment)
#             if lang != 'en':
#                 translated_comment = translator.translate(comment, dest='en').text
#                 translated_comments.append([username, translated_comment])
#             else:
#                 translated_comments.append([username, comment])
#         except Exception as e:
#             print(f"An error occurred during translation: {e}")

#     df = pd.DataFrame(translated_comments, columns=["Username", "Comment"])
#     df.dropna(inplace=True)
#     df.reset_index(drop=True, inplace=True)

#     new_csv_file_path = 'translated_comments.csv'
#     df.to_csv(new_csv_file_path, index=False, encoding="utf-16")

#     return df





# def scrapfyt(url):
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--mute-audio')
#     options.add_argument('--disable-extensions')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--disable-gpu')  # Disable GPU acceleration
#     options.add_argument('--log-level=3')  # Suppress warnings and errors

#     # Initialize the driver
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

#     driver.set_window_size(960, 800)
#     time.sleep(1)
#     driver.get(url)
#     time.sleep(2)

#     try:
#         # Pause YouTube video
#         pause = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))
#         pause.click()
#         time.sleep(0.2)
#         pause.click()
#         time.sleep(4)

#         # Scrolling through all the comments
#         last_height = driver.execute_script("return document.documentElement.scrollHeight")
#         while True:
#             driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#             time.sleep(4)
#             new_height = driver.execute_script("return document.documentElement.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         # Scraping details
#         video_title = driver.find_element(By.NAME, 'title').get_attribute('content')
#         video_owner1 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
#         video_owner = video_owner1[0].text if video_owner1 else 'Unknown'
#         video_comment_with_replies = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text + ' Comments'
#         users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/span')
#         comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

#         csv_file_path = 'comments.csv'
#         with io.open(csv_file_path, 'w', newline='', encoding="utf-16") as file:
#             writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
#             writer.writerow(["Username", "Comment"])
#             for username, comment in zip(users, comments):
#                 writer.writerow([username.text, comment.text])

#     except exceptions.TimeoutException:
#         print("Timeout occurred while scraping comments.")
#         csv_file_path = ''
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         csv_file_path = ''
#     finally:
#         driver.quit()

#     return csv_file_path

# def translate_comments(csv_file_path):
#     translator = Translator()
#     commentsfile = pd.read_csv(csv_file_path, encoding="utf-16")
    
#     translated_comments = []
#     for index, row in commentsfile.iterrows():
#         username = row['Username']
#         comment = row['Comment']
#         try:
#             if pd.isna(comment) or not isinstance(comment, str) or comment.strip() == "":
#                 translated_comments.append([username, comment])
#                 continue
#             lang = detect(comment)
#             if lang != 'en':
#                 translated_comment = translator.translate(comment, dest='en').text
#                 translated_comments.append([username, translated_comment])
#             else:
#                 translated_comments.append([username, comment])
#         except Exception as e:
#             print(f"An error occurred during translation: {e}")
#             translated_comments.append([username, comment])

#     new_csv_file_path = 'translated_comments.csv'
#     with io.open(new_csv_file_path, 'w', newline='', encoding="utf-16") as file:
#         writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
#         writer.writerow(["Username", "Comment"])
#         for row in translated_comments:
#             writer.writerow(row)

#     return new_csv_file_path

# # Usage
# url = 'https://www.youtube.com/watch?v=7n8EzY2GeZU'  # Replace with your URL
# csv_file_path = scrapfyt(url)
# if csv_file_path:
#     print(f"Comments and usernames saved to {csv_file_path}")
#     translated_csv_file_path = translate_comments(csv_file_path)
#     print(f"Translated comments saved to {translated_csv_file_path}")
# else:
#     print("Failed to scrape comments.")

