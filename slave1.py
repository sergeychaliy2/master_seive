import requests
from bs4 import BeautifulSoup
import re

def count_words_on_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        words = re.findall(r'\b\w+\b', soup.get_text(), re.IGNORECASE)
        return len(words)
    except Exception as e:
        print(f"Error in slave 1: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter the URL: ")
    word_count = count_words_on_webpage(url)
    if word_count is not None:
        print(f"Word count in slave 1: {word_count}")
