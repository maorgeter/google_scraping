import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil
import requests


parser = argparse.ArgumentParser(description="Download photos script")
parser.add_argument("--prompt", type=str, required=True, help="Query to search")
parser.add_argument("--how_many", type=int, required=True, help="Number of photos to download")
parser.add_argument("--head", action="store_true", help="Run browser in normal mode (not headless)")

args = parser.parse_args()
prompt = args.prompt
how_many = args.how_many

# Initialize WebDriver and set up the download directory
options = webdriver.ChromeOptions()
if not args.head:
    options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

download_dir = "photos"
if os.path.exists(download_dir):
    shutil.rmtree(download_dir)
os.makedirs(download_dir, exist_ok=True)
valid_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')


def download_image(url, folder, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")


try:
    # Open Google Images and search for a keyword
    driver.get("https://images.google.com/")
    print(f"Searching for {prompt}")

    # Enter search term and start the search
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(prompt)
    search_box.send_keys(Keys.RETURN)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
    time.sleep(2)
    driver.find_element(By.XPATH, f"//div[contains(@jsname, 'dTDiAc')]").click()
    time.sleep(2)
    thumbnails = driver.find_elements(By.XPATH, f"//div[contains(@jsname, 'dTDiAc')]")
    counter = 0
    index = 0
    while counter < how_many and index < len(thumbnails):
        try:
            thumbnail = thumbnails[index]
            thumbnail.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//g-snackbar/following-sibling::div//img"))
            )
            img_src = driver.find_element(By.XPATH, "//g-snackbar/following-sibling::div//img").get_attribute("src")
            start_time = time.time()
            while not img_src.endswith(valid_formats):
                if time.time() - start_time > 4:
                    print("Timeout reached, continuing without valid image.")
                    break  # Exit the loop if 4 seconds have passed
                try:
                    if int(time.time() - start_time) % 2 == 0:
                        img_src = driver.find_element(By.XPATH, "//g-snackbar/following-sibling::div//img").get_attribute(
                            "src")
                    else:
                        img_src = driver.find_element(By.XPATH,
                                                      "//g-snackbar/following-sibling::div//img/preceding-sibling::*").get_attribute(
                            "src")
                except:
                    pass
            if img_src and "http" in img_src:
                download_image(img_src, download_dir, f"{prompt}_{counter + 1}.jpg")
                counter += 1  # Increment only if image is successfully downloaded
            driver.execute_script("arguments[0].scrollIntoView();", thumbnails[index + 2])

        except Exception as e:
            print(f"Error with image {index + 1}")
        finally:
            index += 1  # Move to the next thumbnail


finally:
    driver.quit()
