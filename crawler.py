import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
#from indexing import writer

url_stack=["https://vm009.rz.uos.de/crawl/index.html"]
visited_urls=["https://vm009.rz.uos.de/crawl/index.html"]


schema = Schema(title=TEXT(stored=True), content=TEXT)
# Create an index in the directory indexdr (the directory must already exist!)
ix = create_in("indexdr", schema)
writer = ix.writer()

while len(url_stack) != 0:
    response = requests.get(url_stack.pop())
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.text)
    links = soup.find_all('a', href=True)
    # print('links: ', links)
    # for link in links:
    #     print(link.text)
    for a in links:
        #print('A url: ', url['href'])
        if a['href'].find("html") > 0:
            url = 'https://vm009.rz.uos.de/crawl/' + a['href']
            if url not in visited_urls:
                url_stack.append(url)
                visited_urls.append(url)
                writer.add_document(title=url, content=soup.text)
        # else:
        #     print('we should probs ignore this' + a['href'])
    print(url_stack)
    print(visited_urls)

#TODO: THIS DOESN'T WORK YET
# Retrieving data
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    print('Retrieving')
    # find entries with the words 'first' AND 'last'
    query = QueryParser("content", ix.schema).parse("Page")
    results = searcher.search(query)
    
    # print all results
    for r in results:
        print(r)



# writer.add_document(title=soup.text, content=link)

writer.commit()