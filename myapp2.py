from flask import Flask, request, render_template
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from urllib.parse import urljoin
import traceback


app = Flask(__name__)

@app.route("/")
def startengine():
    
    return render_template('startengine.html')

@app.route("/results")
def results():
    if not 'res' in request.args:
        return 'You tried to hack me'
    else:

        schema = Schema(title=TEXT(stored=True), content=TEXT)

        # # Create an index in the directory indexdr (the directory must already exist!)
        ix = create_in("indexdir", schema)
        # writer = ix.writer()


        # # now let's add some texts (=documents)
        # writer.add_document(title=u"https://vm009.rz.uos.de/crawl/index.html", content=u"This is the first document we've added!")
        # writer.add_document(title=u"https://vm009.rz.uos.de/crawl/index.html", content=u"The second one is even more interesting!")
        # writer.add_document(title=u"'https://vm009.rz.uos.de/crawl/page6.html'", content=u"Page 6 This is Page 6 In a world of pixels and bytes so torn, Lived a quirky platypus and a geeky unicorn. Platypus coded, with fins so deft, While unicorn debugged, with every breath left.")

        # # write the index to the disk
        # writer.commit()

        # Retrieving data
        # with ix.searcher() as searcher:
        #     print('I searched')
        #     # find entries with the words in res
        #     query = QueryParser("content", ix.schema).parse(request.args['res'])
        #     results = searcher.search(query)
        #     print(results)
            
        #     # append all results urls
        #     results_stack = []
        #     for r in results:
        #         results_stack.append(r['title'])
        #     if results_stack == []:
        #         results_stack = ['no results']
        
        # return render_template('results.html', res=results_stack)

        with ix.searcher() as searcher:
            # Split the query into words
            query_words = (request.args['res']).split()
            print('query_words', query_words)
            # Build a query parser for both title and content fields
            query_parser = MultifieldParser(["title", "content"], ix.schema)

            # Initialize the query
            queries = [query_parser.parse(word) for word in query_words]
            print('queries', queries)

            # Perform the search and get the results
            results = [searcher.search(q) for q in queries]
            print('results', results)

            # Return URLs that are in every list
            results_stack = []
            if results:
                common_urls = set(results[0].docs()).intersection(*[set(r.docs()) for r in results[1:]])
                for hit in common_urls:
                    results_stack.append(hit['title', 'content'])
            else:
                return []
            print('results_stack', results_stack)

        return render_template('results.html', res=results_stack)
    

@app.errorhandler(500)
def internal_error(exception):
    return "<pre>"+traceback.format_exc()+"</pre>"

#general structure of forms
# <form action="URL to send the information" method="GET or POST">
#     <input type="text" name="param">
#     <input type="submit"> #creates a submit button. If there is none, pressing "enter" in a text field might also submit the input.
# </form>