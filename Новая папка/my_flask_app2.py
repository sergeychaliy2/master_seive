import re
from bs4 import BeautifulSoup
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/my_unique_api', methods=['POST'])
def my_unique_api_endpoint():
    data = request.json
    url = data.get("requested_url")
    result = {}

    def process_group(group):
        total = 0
        for count in group:
            total += count
        return total

    class MyUniqueMapReduce:
        def __init__(self):
            self.queue = []

        def send(self, key, value):
            self.queue.append((key, value))

        def summarize(self):
            return [process_group(group) for _, group in self.group_by_key()]

        def group_by_key(self):
            grouped = {}
            for key, value in sorted(self.queue, key=lambda x: x[0]):
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(value)
            return grouped.items()

    response = requests.get(url)
    web_text = BeautifulSoup(response.text, "html.parser").get_text()

    x = MyUniqueMapReduce()
    words = re.findall(r'\w+', web_text.lower())
    for word in words:
        x.send(word, 1)

    result = dict(zip(sorted(set(words)), x.summarize()))
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001)
