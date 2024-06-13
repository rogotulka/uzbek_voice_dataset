import requests
from bs4 import BeautifulSoup
import os

# Define the range of post IDs to scrape
start_id = 500
end_id = 505

# Directory to save the text files
output_dir = 'uznews_posts'
os.makedirs(output_dir, exist_ok=True)

for post_id in range(start_id, end_id + 1):
    # Construct the URL for the current post
    post_url = f'https://uznews.uz/posts/{post_id}'
    response = requests.get(post_url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.find('h1').text if soup.find('h1') else 'No Title'

        # Extract content from 'ce-paragraph cdx-block' and 'font-normal text-xl sm:text-lg'
        content = ''
        for paragraph in soup.find_all('div', class_='ce-paragraph cdx-block'):
            content += paragraph.text.strip() + '\n'

        for paragraph in soup.find_all('div', class_='font-normal text-xl sm:text-lg'):
            content += paragraph.text.strip() + '\n'

        # Save the post to a text file
        file_name = os.path.join(output_dir, f'uznews-{post_id}.txt')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n")
            file.write(f"Content:\n{content.strip()}\n")

        print(f"Saved {file_name}")
    else:
        print(f"Failed to fetch post {post_id}: {response.status_code}")

print("Scraping completed.")

