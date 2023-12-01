import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from urllib.parse import urljoin

url_stack = ["https://vm009.rz.uos.de/crawl/index.html"]
visited_urls = set()

schema = Schema(title=TEXT(stored=True), url=TEXT(stored=True), content=TEXT(stored=True))
ix = create_in("indexdir", schema)  # Ensure that the index directory exists
writer = ix.writer()


while url_stack:
    current_url = url_stack.pop(0)

    if current_url not in visited_urls:
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            content = response.text

            soup = BeautifulSoup(content, 'html.parser')
            # print(soup.text)

            body = soup.find('body')
            extract_this = body.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            print('extract_this', extract_this)
            if extract_this:
                extract_this.extract()
            # print('body', body)

            content_preview = ''.join(body.stripped_strings)[:150] + ' ...'
            # print('content_preview', content_preview)

            title = soup.find('title')
            if title:
                title = title.get_text(strip=True)
            else:
                titel = "No Title"

            # Index the page
            writer.add_document(title=title, url=current_url, content=content_preview)

            # Extract links and add to the stack
            links = soup.find_all('a', href=True)
            for a in links:
                if a['href'].endswith("html"):
                    new_url = urljoin(current_url, a['href'])
                    url_stack.append(new_url)
            visited_urls.add(current_url)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {current_url}: {e}")

    # print('url stack:', url_stack)
    # print('visited_urls: ', visited_urls)

# Commit the changes to the index
writer.commit()



