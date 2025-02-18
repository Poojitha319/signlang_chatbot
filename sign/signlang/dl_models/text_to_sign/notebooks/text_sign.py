from nltk import word_tokenize
from nltk.stem import PorterStemmer
import time
from shutil import copyfile
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from ffmpy import FFmpeg
import os
import subprocess
import shlex
from os import startfile
# Constants
SIGN_PATH = r"C:\Users\Sai\Desktop\signsiksha\sign\signlang\dl_models"
DOWNLOAD_WAIT = 7
SIMILARITY_RATIO = 0.9

# Define "useless words"
def useless_words():
    words = {
        "is", "the", "are", "am", "a", "it", "was", "were", "an",
        ",", ".", "?"
    }
    return words

# WebDriver Setup
def create_browser():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for efficiency
    service = FirefoxService()
    browser = webdriver.Firefox(service=service, options=options)
    return browser

# Download sign language video for a word
def download_word_sign(word):
    browser = create_browser()
    browser.get("http://www.aslpro.com/cgi-bin/aslpro/aslpro.cgi")
    first_letter = word[0].lower()
    
    letters = browser.find_elements(By.XPATH, '//a[@class="sideNavBarUnselectedText"]')
    for letter in letters:
        if first_letter == str(letter.text).strip().lower():
            letter.click()
            time.sleep(2)
            break

    spinner = browser.find_elements(By.XPATH, "//option")
    best_score = -1.0
    closest_word_item = None
    for item in spinner:
        item_text = item.text.strip().lower()
        score = similar(word, item_text)
        if score > best_score:
            best_score = score
            closest_word_item = item

    if best_score < SIMILARITY_RATIO:
        print(f"{word} not found in dictionary.")
        browser.quit()
        return None

    real_name = closest_word_item.text.strip().lower()
    print(f"Downloading {real_name}...")
    closest_word_item.click()
    time.sleep(DOWNLOAD_WAIT)
    
    in_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{real_name}.swf")
    out_path = os.path.join(SIGN_PATH, f"{real_name}.mp4")
    convert_file_format(in_path, out_path)
    browser.quit()
    return real_name

# Convert SWF to MP4
def convert_file_format(in_path, out_path):
    ff = FFmpeg(inputs={in_path: None}, outputs={out_path: None})
    ff.run()

# Get available videos in the database
def get_words_in_database():
    vids = os.listdir(SIGN_PATH)
    return [v[:-4] for v in vids if v.endswith(".mp4")]

# Process text into meaningful words
def process_text(text):
    words = word_tokenize(text)
    useful_words = [w.lower() for w in words if w.lower() not in useless_words()]
    return useful_words

# Merge videos into one output
def merge_signs(words):
    with open("vidlist.txt", 'w') as f:
        for w in words:
            f.write(f"file '{os.path.join(SIGN_PATH, w)}.mp4'\n")

    command = "ffmpeg -f concat -safe 0 -i vidlist.txt -c copy output.mp4 -y"
    args = shlex.split(command)
    process = subprocess.Popen(args)
    process.wait()

    out_path = os.path.join(SIGN_PATH, "Output", "out.mp4")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    copyfile("output.mp4", out_path)
    os.remove("output.mp4")

# Check if word is in the database
def find_in_db(word):
    db_list = get_words_in_database()
    best_score = -1.0
    best_vid_name = None
    for vid in db_list:
        score = similar(word, vid)
        if score > best_score:
            best_score = score
            best_vid_name = vid
    return best_vid_name if best_score > SIMILARITY_RATIO else None

# Calculate similarity between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Main script
if __name__ == "__main__":
    text = "B C D"
    print(f"Text: {text}")
    
    # Process text
    words = process_text(text)
    
    # Download words not in the database
    real_words = []
    for word in words:
        real_name = find_in_db(word)
        if real_name:
            print(f"{word} is already in database as {real_name}")
            real_words.append(real_name)
        else:
            downloaded_name = download_word_sign(word)
            if downloaded_name:
                real_words.append(downloaded_name)
    
    # Merge videos
    merge_signs(real_words)
    print("Video generation complete!")

    # Play the video
    startfile(os.path.join(SIGN_PATH, "Output", "out.mp4"))



