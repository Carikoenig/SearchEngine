import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from urllib.parse import urljoin

url_stack = ["https://vm009.rz.uos.de/crawl/index.html"]
visited_urls = set()

schema = Schema(title=TEXT(stored=True), content=TEXT)
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
            print(soup.text)

            # Index the page
            writer.add_document(title=current_url, content=soup.text)

            # Extract links and add to the stack
            links = soup.find_all('a', href=True)
            for a in links:
                if a['href'].endswith("html"):
                    new_url = urljoin(current_url, a['href'])
                    url_stack.append(new_url)
                    visited_urls.add(new_url)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {current_url}: {e}")

# Commit the changes to the index
writer.commit()

# Query parser and search
def search(query_string):
    with ix.searcher() as searcher:
        # Split the query into words
        query_words = query_string.split()

        # Build a query parser for both title and content fields
        query_parser = MultifieldParser(["title", "content"], ix.schema)

        # Initialize the query
        queries = [query_parser.parse(word) for word in query_words]

        # Perform the search and get the results
        results = [searcher.search(q) for q in queries]

        # Return URLs that are in every list
        if results:
            common_urls = set(results[0].docs()).intersection(*[set(r.docs()) for r in results[1:]])
            return [hit["title"] for hit in common_urls]
        else:
            return []



# writer.add_document(title=soup.text, content=link)

writer.commit()
