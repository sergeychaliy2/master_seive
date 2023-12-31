FROM ubuntu:latest 

RUN apt-get update && apt-get -y install python3 python3-pip
RUN python3 -m pip install beautifulsoup4 flask requests pymorphy2

COPY my_flask_app.py my_flask_app.py
COPY my_flask_app2.py my_flask_app2.py
COPY my_data_collector.py my_data_collector.py

EXPOSE 8000
