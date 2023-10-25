import requests
from bs4 import BeautifulSoup
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def count_specific_words_on_webpage(url, specific_words):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        word_count = {}

        for word in specific_words:
            normalized_word = morph.parse(word)[0].normal_form
            count = len(re.findall(rf'\b{normalized_word}\b', text, re.IGNORECASE))
            if count > 0:
                word_count[normalized_word] = count

        return word_count
    except Exception as e:
        print(f"Error in slave 2: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter the URL: ")
    specific_words = input("Enter words: ").split(',')
    specific_word_count = count_specific_words_on_webpage(url, specific_words)

    if specific_word_count is not None:
        print("Word count for specific words in slave 2:")
        for word, count in specific_word_count.items():
            print(f"'{word}': {count}")
