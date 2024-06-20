import requests
from bs4 import BeautifulSoup
import os
from langdetect import detect, DetectorFactory
from requests.exceptions import RequestException

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Define the starting and ending post IDs
start_id = 725
end_id = 74300

# Directory to save the text files
output_dir = 'all'
os.makedirs(output_dir, exist_ok=True)

post_id = start_id
while post_id <= end_id:
    try:
        # Construct the URL for the current post
        post_url = f'https://uznews.uz/posts/{post_id}'
        response = requests.get(post_url)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_element = soup.find('h1', class_='font-bold md:text-3xl text-2xl my-2')
            title_text = title_element.text.strip() if title_element else 'No Title'

            # Extract subtitle
            subtitle_element = soup.find('p', class_='font-normal text-xl sm:text-lg')
            subtitle_text = subtitle_element.text.strip() if subtitle_element else 'No Subtitle'

            # Extract main text
            main_text = ''
            main_text_elements = soup.find_all('div', class_='ce-paragraph cdx-block')
            for paragraph in main_text_elements:
                main_text += paragraph.text.strip() + '\n'

            # Combine title, subtitle, and main text for language detection
            full_text = f"{title_text}\n{subtitle_text}\n{main_text.strip()}"

            # Detect language
            try:
                detected_language = detect(full_text)
            except Exception as e:
                detected_language = 'unknown'
                print(f"Language detection failed for post {post_id}: {e}")

            # Save the post only if it is not detected as Russian
            if detected_language != 'ru':
                file_name = os.path.join(output_dir, f'uznews-{post_id}.txt')
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(f"Language: {detected_language}\n")
                    file.write(f"Title: {title_text}\n")
                    file.write(f"Subtitle: {subtitle_text}\n")
                    file.write(f"Content:\n{main_text.strip()}\n")

                print(f"Saved {file_name}")
            else:
                print(f"Skipped post {post_id} (detected language: {detected_language})")
        elif response.status_code == 404:
            if post_id >= end_id:
                print(f"No more posts found. Stopping at post ID {post_id}.")
                break
            else:
                print(f"Post {post_id} not found (404). Skipping.")
        else:
            print(f"Failed to fetch post {post_id}: HTTP {response.status_code}")

    except RequestException as e:
        print(f"Request failed for post {post_id}: {e}")
    except Exception as e:
        print(f"An error occurred for post {post_id}: {e}")

    post_id += 1

print("Scraping completed.")
