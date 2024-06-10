"""
use requests library
forget html tags
use html library for getting text from the elements

"""
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                logging.info(f"Reached the end of available articles with URL: {url}")
            else:
                logging.error(f"Request failed: {e}")
            return None

    def extract_text_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find('div', class_='news-article')  # Modify this based on the website structure
        if article:
            title = article.find('h1').get_text(strip=True) if article.find('h1') else "No Title"
            content = article.find('div', class_='news-article-content').get_text(strip=True) if article.find('div', class_='news-article-content') else "No Content"
            return title, content
        return None, None

    def save_text_to_file(self, title, content, filename):
        try:
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(f"Title: {title}\n")
                file.write(f"Content: {content}\n\n")
            logging.info(f"Saved article: {title}")
        except IOError as e:
            logging.error(f"File write failed: {e}")

    def run(self, start_id, end_id):
        for article_id in range(start_id, end_id + 1):
            url = urljoin(self.base_url, f'/posts/{article_id}')
            logging.info(f"Fetching URL: {url}")
            html_content = self.get_html(url)
            if html_content:
                title, content = self.extract_text_from_html(html_content)
                if title and content:
                    self.save_text_to_file(title, content, 'news_articles.txt')
            else:
                break  # Stop the loop if a 404 error is encountered

if __name__ == "__main__":
    # Example usage
    base_url = 'https://uznews.uz'
    start_id = 500  # Starting article ID
    end_id = 74234  # Set a high upper limit to ensure we get all articles until 404
    scraper = NewsScraper(base_url)
    scraper.run(start_id, end_id)
