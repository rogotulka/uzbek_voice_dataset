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
    blog_posts = []

    for blog_url in blog_urls:
        blog_response = requests.get(blog_url)
        if blog_response.status_code == 200:
            blog_soup = BeautifulSoup(blog_response.content, 'html.parser')

            # Extract title
            title = blog_soup.find('h1').text if blog_soup.find('h1') else 'No Title'

            # Extract content
            content = ''
            for paragraph in blog_soup.find_all('p'):
                content += paragraph.text + '\n'

            # Save the blog post data
            blog_posts.append({
                'url': blog_url,
                'title': title,
                'content': content.strip()
            })

    # Step 5: Display or process the blog posts
    for post in blog_posts:
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Content: {post['content']}...")  # Display content
        print('-' * 80)
else:
    print(f"Failed to fetch the blog listing page: {response.status_code}")
