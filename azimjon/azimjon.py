import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the blog listing page
blog_listing_url = 'https://azimjon.com/blog/'
response = requests.get(blog_listing_url)

if response.status_code == 200:
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 3: Extract the links to individual blog posts
    blog_links = soup.find_all('a', href=True)
    blog_urls = [link['href'] for link in blog_links if '/blog/' in link['href']]

    # Remove duplicates and ensure full URLs
    blog_urls = list(set(['https://azimjon.com' + url for url in blog_urls]))

    # Step 4: Scrape each individual blog post
    for index, blog_url in enumerate(blog_urls, start=1):
        blog_response = requests.get(blog_url)
        if blog_response.status_code == 200:
            blog_soup = BeautifulSoup(blog_response.content, 'html.parser')

            # Extract title
            title = blog_soup.find('h1').text if blog_soup.find('h1') else 'No Title'

            # Extract content
            content = ''
            for paragraph in blog_soup.find_all('p'):
                paragraph_text = paragraph.text.strip()
                # Skip paragraphs that match the unwanted footer text
                if paragraph_text.startswith('© 2024 azimjon.com'):
                    continue
                content += paragraph_text + '\n'

            # Write to a file
            file_name = f'azimjon-blog-{index}.txt'
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(f"{title}")
                file.write(f"{content.strip()}\n")

            print(f"Saved {file_name}")

else:
    print(f"Failed to fetch the blog listing page: {response.status_code}")
