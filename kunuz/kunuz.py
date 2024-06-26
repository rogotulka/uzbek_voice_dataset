import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the website
base_url = "https://kun.uz"


# Function to get all category links from the homepage
def get_category_links():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all category links (update the class name based on actual HTML)
    categories = soup.find_all('a', class_='category-link')
    category_links = [base_url + category['href'] for category in categories]

    return category_links


# Function to get all article links from a category page, including pagination
def get_all_article_links(category_url):
    article_links = []
    page_number = 1

    while True:
        paginated_url = f"{category_url}/page/{page_number}"
        response = requests.get(paginated_url)

        # If the page doesn't exist, break the loop
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all article links on the category page (update the class name based on actual HTML)
        articles = soup.find_all('a', class_='news-link')

        # If no articles are found, break the loop
        if not articles:
            break

        article_links.extend([base_url + article['href'] for article in articles])
        page_number += 1

    return article_links


# Function to scrape details of an individual article
def scrape_article(article_url):
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')

    title = article_soup.find('h1', class_='title').get_text(strip=True)
    date = article_soup.find('time', class_='publish-date').get_text(strip=True)
    content = article_soup.find('div', class_='content').get_text(strip=True)

    return {
        'title': title,
        'date': date,
        'content': content,
        'url': article_url
    }


# Main function to orchestrate the scraping process
def main():
    category_links = get_category_links()
    all_article_links = []

    for category_link in category_links:
        all_article_links.extend(get_all_article_links(category_link))

    articles_data = []

    for article_link in all_article_links:
        articles_data.append(scrape_article(article_link))

    # Save the scraped data to a CSV file
    df = pd.DataFrame(articles_data)
    df.to_csv('kun_uz_articles.csv', index=False)
    print("Data saved to kun_uz_articles.csv")


# Execute the main function
if __name__ == "__main__":
    main()
