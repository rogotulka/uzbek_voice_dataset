import requests
from bs4 import BeautifulSoup
import os

BASE_URL = 'https://kun.uz'

def get_category_urls():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.select('ul.page-header__menu.reset-list a')
    category_urls = {category.text.strip(): BASE_URL + category['href'] for category in categories if 'href' in category.attrs}
    return category_urls

def get_post_urls(category_url):
    post_urls = []
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.select('a.news__title')
    post_urls.extend([BASE_URL + post['href'] for post in posts if 'href' in post.attrs])
    next_page = soup.select_one('a.next_page')
    while next_page:
        response = requests.get(BASE_URL + next_page['href'])
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('a.news__title')
        post_urls.extend([BASE_URL + post['href'] for post in posts if 'href' in post.attrs])
        next_page = soup.select_one('a.next_page')
    return post_urls

def scrape_post(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', class_='single-header__title')
    date_element = soup.find('div', class_='single-header__date')
    content_element = soup.find('div', class_='single-content')

    title = title_element.text.strip() if title_element else 'No Title'
    date = date_element.text.strip() if date_element else 'No Date'
    content = content_element.text.strip() if content_element else 'No Content'

    return {
        'title': title,
        'date': date,
        'content': content
    }

def save_post_to_file(post_details, directory):
    filename = f"{post_details['title']}.txt"
    valid_filename = ''.join(char for char in filename if char.isalnum() or char in (' ', '.', '_')).rstrip()
    filepath = os.path.join(directory, valid_filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(f"Title: {post_details['title']}\n")
        file.write(f"Date: {post_details['date']}\n")
        file.write(f"Content:\n{post_details['content']}\n")

save_directory = 'scraped_posts'
os.makedirs(save_directory, exist_ok=True)

category_urls = get_category_urls()
all_posts = []

for category, url in category_urls.items():
    post_urls = get_post_urls(url)
    for post_url in post_urls:
        post_details = scrape_post(post_url)
        save_post_to_file(post_details, save_directory)
        all_posts.append(post_details)

print(f"Scraped and saved {len(all_posts)} posts.")
