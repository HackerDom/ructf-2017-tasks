#!/usr/bin/env python3

import os
import time

from bs4 import BeautifulSoup as bs
import requests


USERS_FILE_LOCATION = 'users.txt'
DELAY_SECONDS = 0.5
ADDRESS = os.environ.get('TASK_ADDRESS', 'http://3ch.ructf.org')
PICTURES = [
    'https://i.ytimg.com/vi/B2O-RdVgT24/hqdefault.jpg',
]


current_picture = 0


class User:
    def __init__(self, username, passwd, motto):
        self.username = username
        self.passwds = [ passwd ]
        self.images = []
        self.motto = motto


def load_users(users_file):
    result = []
    with open(users_file, 'rt') as f:
        lines = f.readlines()
    for line in lines:
        username, passwd, motto = line.strip().split(':')
        result.append(User(username, passwd, motto))
    return result


def get_signin_url(base_address, user):
    return "%s/signin?username=%s&passwd=%s" % (base_address, user.username, user.passwds[0])


def get_addimg_url(base_address, src):
    return "%s/addimg?src=%s" % (base_address, src)


if __name__ == "__main__":
    users = [ user for user in load_users(USERS_FILE_LOCATION) if user.username.startswith('m00t_') ]


    while True:
        pic = PICTURES[current_picture]
        current_picture = (current_picture + 1) % len(PICTURES)

        for user in users:
            jar = requests.cookies.RequestsCookieJar()
            response = requests.get(get_signin_url(ADDRESS, user), cookies=jar)
            if response.status_code != requests.codes.ok:
                print("Failed to login into user %s: server returned status %d" % (user.username, response.status_code))
                continue

            soup = bs(response.text, "lxml")
            for image in soup.findAll("img"):
                requests.get(image["src"], cookies=jar)


            response = requests.get(get_addimg_url(ADDRESS, pic), cookies=jar)
            if response.status_code != requests.codes.ok:
                print("Failed to add image: server returned status %d" % response.status_code)
                continue

            time.sleep(DELAY_SECONDS)
