import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(5)  # Wait for login to complete

def fetch_comments(url, driver):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver.get(url)
    time.sleep(5)  # Initial wait for the page to load
    
    df = pd.DataFrame()  # Initialize df at the start of the function
    
    try:
        # Scroll to load comments
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        comments = []
        usernames = []

        print("Locating comments...")
        comment_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.break-words'))
        )
        for element in comment_elements:
            comments.append(element.text)

        print("Locating usernames...")
        username_elements = driver.find_elements(By.CSS_SELECTOR, 'span.ember-view.t-bold')
        for element in username_elements:
            usernames.append(element.text)

        print(f"Fetched {len(comments)} comments and {len(usernames)} usernames")

        if comments and usernames:
            df = pd.DataFrame({
                'Username': usernames,
                'Comment': comments
            })

        print("DataFrame created:")
        print(df)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return df

if __name__ == "__main__":
    # Example usage
    url = 'https://www.linkedin.com/posts/himanshu-dutta-257875179_all-gate-2024-toppers-congratulations-activity-7198903415484121088-1wba?utm_source=share&utm_medium=member_desktop'
    email = 'susamerica100@gmail.com'
    password = 'projectwork'
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    linkedin_login(driver, email, password)
    
    comments_df = fetch_comments(url, driver)
    if not comments_df.empty:
        comments_df.to_csv("comments.csv", index=False)
        print("Comments saved to comments.csv")
    else:
        print("No comments found.")
