import requests
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

requested_url = input("Введите URL для анализа: ")
url_payload = {
    "requested_url": requested_url
}

result = requests.post("http://127.0.0.1:8000/my_unique_api", json=url_payload).json()

for word, count in sorted(result.items(), key=lambda x: x[1], reverse=True):
    print(word, count)

user_word_input = input("Введите слово для вывода результата: ").lower()
user_word = morph.parse(user_word_input)[0]

if user_word.normal_form in result:
    print(f"Результат для слова '{user_word_input}': {result[user_word.normal_form]}")
    print("Варианты слова в различных падежах, найденные в тексте:")
    for case in ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']:
        inflected_word = user_word.inflect({case})
        if inflected_word and inflected_word.word in result:
            print(f"{case.capitalize()}: {result[inflected_word.word]}")
else:
    print(f"Слово '{user_word_input}' не найдено в тексте.")
