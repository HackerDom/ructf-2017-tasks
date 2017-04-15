from python:3.6-slim

run mkdir -p /home/3ch \
    && pip install beautifulsoup4 requests lxml

copy . /home/3ch/

workdir /home/3ch
cmd ./main.py
