# Project 1: Build a search engine

Acces to finished project: NEED TO BE CONNECTED TO UNIVERSITYS VPN!! 
    
    http://vm322.rz.uni-osnabrueck.de/user097/myapp2.wsgi/
    
OR: 

    download this repository on local pc
    create a venv and install the requirements with "pip install -r requirements.txt"
    run the crawler with "python crawler.py" to create the index
    run the flask app with "flask --app myapp2.py run"
    
# Instructions for creating project

Build a search engine with all four components:

    Crawler
    Index
    Query parser and search algorithm
    User Frontend


Demonstrate it by crawling one website and making its content available to the user via a web frontend with a simple search form. 

Make the result available on the provided demo server.

Submit the code and the link to the demo deployment.

 

Suggested order of building:

 

Week 1 of project:

    Create a working environment on your computers
    Create a repository (Gitlab, Github, …) for your project 1 and make sure all group members can access it
    Start with adding a .gitignore and a requirements.txt file to the repository (requirements are requests and beautifulsoup4)
    Create a `crawler.py` file and define the skeleton of the crawling algorithm: 
        Crawl (=get and parse) all HTML pages on a certain server 
        that can directly or indirectly be reached from a start URL 
        by following links on the pages. 
        Do not follow links to URLs on other servers and only process HTML responses. 
        Test the crawler with a simple website, e.g., https://vm009.rz.uos.de/crawl/index.html 
    Build an in-memory index from the HTML text content found. 
        The most straightforward index is a dictionary with words as keys and lists of URLs that refer to pages that include the word.
    Add a function 'search' that takes a list of words as a parameter and returns (by using the index) a list of links to all pages that contain all the words from the list. 
    Test the functionality.

 

Don't worry if you don't get that far! Use the element chat and the Friday session to ask questions, report problems and tell about hurdles and obstacles!

 

Week 2:

    Replace the simple index with code using the woosh library ( will be introduced in week 3 - https://whoosh.readthedocs.io/en/latest/intro.html ).
    Build a flask app (will be introduced in week 3 - ) with two URLs that shows the following behaviour:
        GET home URL: Show search form
        GET search URL with parameter q: Search for q using the index and display a list of URLs as links

 

Week 3:

    Improve the index by adding information (ideas will be presented in week 4)
    Improve the output by including title and teaser text
    Install your search engine on the demo server provided (will be introduced in week 4)

 

Beginn: 27.10.2023, 12:00
Ende: 17.11.2023, 12:00

Kurs: Artificial Intelligence and the Web (8.3108)
Semester: WiSe 2023/24
Lehrende: Dr. phil. Tobias Thelen 
