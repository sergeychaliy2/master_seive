FROM ubuntu:latest 

RUN apt-get update && apt-get -y install python3 python3-pip
RUN python3 -m pip install beautifulsoup4 flask requests pymorphy2

COPY my_flask_app.py my_data_collector.py
