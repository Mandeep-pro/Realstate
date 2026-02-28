import threading
import requests
from bs4 import BeautifulSoup


urls=[
    'https://www.example.com', 
    'https://www.wikipedia.org', 
    'https://www.python.org']

def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    print(f"Title of {url}: {title}")

    ## print the length of the content
    print(f"Content length of {url}: {len(response.content)} bytes")    

threads = []
for url in urls:
    thread = threading.Thread(target=fetch_url, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Finished fetching all URLs.")