from whoosh import index
from whoosh.qparser import MultifieldParser

ix = index.open_dir('indexdir') 

# Query parser and search
def search(query_string):
    with ix.searcher() as searcher:
        # Split the query into words
        query_words = query_string.split()

        # Build a query parser for both title and content fields
        query_parser = MultifieldParser(["title", "content"], ix.schema)

        # Initialize the query
        queries = [query_parser.parse(word) for word in query_words]
        print('queries', queries)


        # Perform the search and get the results
        results = [searcher.search(q) for q in queries]
        print('results', results)

        # Extract document IDs from each result set
        doc_ids_sets = [set(result.docs()) for result in results]

        # Find the intersection of document IDs
        common_doc_ids = set.intersection(*doc_ids_sets)

        # Retrieve titles for common document IDs
        common_titles = [searcher.stored_fields(doc_id)["title"] for doc_id in common_doc_ids]

        return common_titles

# results = search('unicorn')
# print('results: ', results)