FROM python:3.8

RUN pip install requests beautifulsoup4 pymorphy2

WORKDIR /app

COPY . /app

CMD ["python", "master.py"]
