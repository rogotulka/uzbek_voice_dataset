import requests
from bs4 import BeautifulSoup
import os
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from requests.exceptions import RequestException
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, local
from UzTransliterator import UzTransliterator

DetectorFactory.seed = 0

start_id = 1
end_id = 74700
num_threads = 10  # Number of threads to use
uztrans = UzTransliterator.UzTransliterator()  #uztrans

# Directory to save the text files
output_dir = 'latin'
os.makedirs(output_dir, exist_ok=True)

# List to store titles
titles = []
titles_lock = Lock()  # Lock to ensure thread safety for the titles list
langdetect_lock = Lock()  # Lock for language detection to ensure thread safety

# Thread-local storage for language detector
thread_local = local()

def detect_language(text):
    with langdetect_lock:
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'

def fetch_post(post_id):
    try:
        # Construct the URL for the current post
        post_url = f'https://uznews.uz/posts/{post_id}'
        response = requests.get(post_url)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            title_element = soup.find('h1', class_='font-bold md:text-3xl text-2xl my-2')
            title_text = title_element.text.strip() if title_element else 'No Title'

            subtitle_element = soup.find('p', class_='font-normal text-xl sm:text-lg')
            subtitle_text = subtitle_element.text.strip() if subtitle_element else 'No Subtitle'

            main_text = ''
            main_text_elements = soup.find_all('div', class_='ce-paragraph cdx-block')
            for paragraph in main_text_elements:
                main_text += paragraph.text.strip() + '\n'

            # Combine title, subtitle, and main text for language detection
            full_text = f"{title_text}\n{subtitle_text}\n{main_text.strip()}"

            # Detect language
            detected_language = detect_language(full_text)

            # Save the post only if it is not detected as Russian
            if detected_language != 'ru':
                file_name = os.path.join(output_dir, f'uznews-{post_id}.txt')
                with open(file_name, 'w', encoding='utf-8') as file:
                    title_text = uztrans.transliterate(title_text, from_="cyr", to="lat")
                    subtitle_text = uztrans.transliterate(subtitle_text, from_="cyr", to="lat")
                    main_text = uztrans.transliterate(main_text, from_="cyr", to="lat")
                    file.write(f"{subtitle_text}\n")
                    file.write(f"{main_text.strip()}\n")

                # Add title to the list of titles (with thread safety)
                with titles_lock:
                    titles.append(title_text)
                print(f"Saved {file_name}")
            else:
                print(f"Skipped post {post_id} (detected language: {detected_language})")
        elif response.status_code == 404:
            print(f"Post {post_id} not found (404). Skipping.")
        else:
            print(f"Failed to fetch post {post_id}: HTTP {response.status_code}")

    except RequestException as e:
        print(f"Request failed for post {post_id}: {e}")
    except Exception as e:
        print(f"An error occurred for post {post_id}: {e}")

    return post_id

# Using ThreadPoolExecutor to fetch posts in parallel
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(fetch_post, post_id) for post_id in range(start_id, end_id + 1)]
    for future in as_completed(futures):
        future.result()

# Write titles to a CSV file
csv_file_path = os.path.join(output_dir, 'titles.csv')
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Title'])
    with titles_lock:
        for title in titles:
            csv_writer.writerow([title])

print("Scraping completed.")
print(f"Titles saved to {csv_file_path}.")
