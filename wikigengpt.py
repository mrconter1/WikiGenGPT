import http.server
import socketserver
import urllib.parse
import threading
import argparse

import subprocess
import openai
import re
import os

openai.api_key = "YOUR_API_KEY"

template_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample Wikipedia Article</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            background-color: #181818;
            color: #f0f0f0;
        }

        h1 {
            font-size: 32px;
        }

        h2 {
            font-size: 24px;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }

        p {
            margin-top: 0.5em;
            margin-bottom: 1em;
        }

        ul, ol {
            padding-left: 20px;
        }

        a {
            color: #1e90ff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Sample Wikipedia Article</h1>
    <p>This is a sample Wikipedia article page. It is designed to resemble the appearance of a typical Wikipedia article.</p>

    <h2>Contents</h2>
    <ol>
        <li><a href="#section1">Section 1</a></li>
        <li><a href="#section2">Section 2</a>
            <ol>
                <li><a href="#subsection2.1">Subsection 2.1</a></li>
                <li><a href="#subsection2.2">Subsection 2.2</a></li>
            </ol>
        </li>
        <li><a href="#section3">Section 3</a></li>
    </ol>

    <h2 id="section1">Section 1</h2>
    <p>This is the content for Section 1. Wikipedia articles are divided into different sections to make it easier for readers to find and navigate through the information they are looking for.</p>

    <h2 id="section2">Section 2</h2>
    <p>This is the content for Section 2. Sections can be further divided into subsections for better organization and clarity.</p>

    <h3 id="subsection2.1">Subsection 2.1</h3>
    <p>This is the content for Subsection 2.1. Subsections provide a more granular division of the content within a section.</p>

    <h3 id="subsection2.2">Subsection 2.2</h3>
    <p>This is the content for Subsection 2.2. Subsections can be used to break down complex topics into smaller, more digestible parts.</p>

    <h2 id="section3">Section 3</h2>
    <p>This is the content for Section 3. In a real Wikipedia article, each section would contain more detailed and comprehensive information about the topic being covered.</p>
</body>
</html>

"""




# Create the parser
parser = argparse.ArgumentParser(description='Process some variables.')

# Add the user_concept argument
parser.add_argument('user_concept', type=str, help='A user concept for the HTML page')

# Parse the arguments
args = parser.parse_args()

# Now you can use args.user_concept in your script
user_concept = args.user_concept

# Only set custom_html if user_concept is provided
if user_concept is not None:
    custom_html = template_page + """Could you please use the HTML template above to do the following? Write an EXTREMELY interesting and intriguing made-up Wikipedia article about {user_concept}. It should have a Wikipedia-like name for the article. It could be about engineering, people, events, or whatever. It should sound real but should actually be real. Also make sure to add Wikipedia links throughout the article text just like a real Wikipedia article would have. The article should not mention that it is fictional but rather look totally real (even though it's not). Also,  make sure that the links only link to other non-real things. It cannot for instance link to "car" because that actually exists. There should be at least ten links. Make sure to never use the word "fantasy" or "fiction". Make sure that all the links are snake_case! The links should also be relative. All the html-files will be located in the same folder! Don't use ":" or "-" in the title. The title should be Wikipedia-like. The links should not end in ".html"! Avoid colon in the titles! Never use ":" in the title of an article!!! Never use use a "#" in the hyperlinks!!!""".format(user_concept=user_concept)
    start_html = custom_html
else:
    start_html = template_page + """Could you please use the HTML template above to do the following? Write an EXTREMELY interesting and intriguing made-up Wikipedia article about something. It should have a Wikipedia-like name for the article. It could be about engineering, people, events, or whatever. It should sound real but should actually be real. Also make sure to add Wikipedia links throughout the article text just like a real Wikipedia article would have. The article should not mention that it is fictional but rather look totally real (even though it's not). Also,  make sure that the links only link to other non-real things. It cannot for instance link to "car" because that actually exists. There should be at least ten links. Make sure to never use the word "fantasy" or "fiction". Make sure that all the links are snake_case! The links should also be relative. All the html-files will be located in the same folder! Don't use ":" or "-" in the title. The title should be Wikipedia-like. The links should not end in ".html"! Avoid colon in the titles! Never use ":" in the title of an article!!! Never use use a "#" in the hyperlinks!!!"""

new_html = template_page + """Given the context of XXXXXXXXXX this other article write a NEW EXTREMELY interesting and intriguing made-up Wikipedia article about it. It should sound real but should actually be real. Also make sure to add Wikipedia links throughout the article text just like a real Wikipedia article would have. The article should not mention that it is fictional but rather look totally real (even though it's not). Also,  make sure that the links only link to other non-real things. It cannot for instance link to "car" because that actually exists. There should be at least ten links. Make sure to never use the word "fantasy" or "fiction". Make sure that all the links are snake_case! The links should also be relative. All the html-files will be located in the same folder! Don't use ":" or "-" in the title. The title should be Wikipedia-like. The links should not end in ".html"! Avoid colon in the titles! Never use ":" in the title of an article!!! Never use use a "#" in the hyperlinks!!!"""

def create_response(msg):

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    messages.append({"role": "user", "content": msg})
    
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

    response_str = response['choices'][0]['message']['content']

    return response_str

def generate_new_page():

    return create_response(start_html)

def generate_page(title):

    modified_prompt = new_html.replace("XXXXXXXXXX", title)

    return create_response(modified_prompt)

def extract_hyperlinks(html):
    links = []
    start_tag = '<a href="'
    end_tag = '"'

    index = html.find(start_tag)
    while index != -1:
        start = index + len(start_tag)
        end = html.find(end_tag, start)
        link = html[start:end]
        if "#" not in link:
            links.append(link)

        index = html.find(start_tag, end)

    return links

def extract_title_and_convert_to_snake_case(html_string):
    title_pattern = re.compile(r'<title>(.*?)<\/title>', re.IGNORECASE)
    match = title_pattern.search(html_string)
    if match:
        title = match.group(1)
    else:
        return None

    title = re.sub(r'\s+', '_', title) 
    title = re.sub(r'[^A-Za-z0-9_]', '', title)
    title = title.lower() 

    return title

def save_article(name, html):
    with open(name + ".html", "w") as out_file:
        out_file.write(html)
    print(name + " has been created!")

def load_page(name):
    html = ""
    with open(name + ".html") as f:
        html = f.read()
    return html

def read_pages():
    pages = []
    files_in_current_folder = os.listdir()
    for file in files_in_current_folder:
        if file.endswith(".html"):
            only_name = file.split(".")[0]
            pages.append(only_name)
    return pages

def generate_articles_for_links(links):
    for link in links:
        page = generate_page(link)
        relative_url = extract_title_and_convert_to_snake_case(page)
        save_article(relative_url, page)

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urllib.parse.urlparse(self.path).path
        parsed_url = parsed_url[1:]
        if parsed_url in read_pages():
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            page_html = load_page(parsed_url)
            self.wfile.write(page_html.encode())
            links = extract_hyperlinks(page_html)
            generate_new_links_thread = threading.Thread(target=generate_articles_for_links, args=(links,))
            generate_new_links_thread.start()
            return
        else:
            # Serve the requested file
            super().do_GET()

# Define the handler to use for incoming requests
Handler = MyRequestHandler

# Generate first page
first_page = generate_new_page()
relative_url = extract_title_and_convert_to_snake_case(first_page)
save_article(relative_url, first_page)
print("http://localhost:8080/" + relative_url)

# Start the server
port = 8080
httpd = socketserver.TCPServer(("", port), Handler)
print("Serving on port", port)
httpd.serve_forever()