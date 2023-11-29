from flask import Flask, request, render_template
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from urllib.parse import urljoin
import traceback
from searching import search


app = Flask(__name__)

@app.route("/")
def startengine():
    
    return render_template('startengine.html')

@app.route("/results")
def results():
    if not 'res' in request.args:
        return 'You tried to hack me'
    else:
        titles = search(request.args['res'])
        return render_template('results.html', res=titles)
    

@app.errorhandler(500)
def internal_error(exception):
    return "<pre>"+traceback.format_exc()+"</pre>"

