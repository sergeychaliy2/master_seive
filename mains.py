import requests
from bs4 import BeautifulSoup
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# slave_1
def count_words_on_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        words = re.findall(r'\b\w+\b', soup.get_text(), re.IGNORECASE)
        return len(words)
    except Exception as e:
        print(f"Error: {e}")
        return None

# slave_2
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
        print(f"Error: {e}")
        return None

# Функция для поиска похожих слов
def find_similar_words(word):
    parsed_word = morph.parse(word)[0]
    return [parsed_word.normal_form] + [inflection.word for inflection in parsed_word.lexeme]

# master
def word_count_wizard():
    url = input("Enter the URL: ")
    specific_words = input("Enter words: ").split(',')
    word_count = count_words_on_webpage(url)
    specific_word_count = count_specific_words_on_webpage(url, specific_words)

    if word_count is not None:
        print(f"Word count: {word_count}")

    if specific_word_count is not None:
        print("Word count for specific words:")
        for word, count in specific_word_count.items():
            print(f"'{word}': {count}")
            similar_words = find_similar_words(word)
            print(f"Similar words: {', '.join(similar_words)}")

if __name__ == "__main__":
    word_count_wizard()
