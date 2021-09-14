# !/usr/bin/python
# -*- coding: utf-8 -*-

# MIT License
# 
# Copyright (c) 2021 ITyouG(George Guan)
# https://github.com/ITyouG/Fortinet-Auth-Login
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time
import requests
from requests import post, head, Session, ConnectionError
from os import path


googleUrl = "http://www.google.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}


class FirewallState:
    Fail, Login, BadAuth, Retry, Keepalive, Error = list(range(6))


def login_func(username, password):
    print("do login.")
    try:
        # head(googleUrl)
        session = Session()
        res = session.get(googleUrl, headers=headers, timeout=3)

        print("http_Status_Code:", res.status_code)

        if res.history[0].status_code != 303:
            print('Already connected. :)')
            return FirewallState.Login
        else:
            magic = res.url.split('?')[1]
            payload = {
                '4Tredir': 'http://google.com/',
                'magic': str(magic),
                'username': username,
                'password': password,
            }

            url_2 = 'http://192.168.201.6:1000/'
            res = post(url_2, headers=headers, data=payload, timeout=3)

            fgt_keepalive_url = res.url
            print(fgt_keepalive_url)

            return FirewallState.Keepalive
    except ConnectionError:
        print('ConnectionError - login_func. :(')
        return FirewallState.Fail


def keepalive_func():
    print("do keepalive.")
    try:
        url = "http://172.22.6.254:1000/keepalive?040106060a020104"
        response = requests.request("GET", url)
        if response.status_code == 200:
            print('Already keepalive. :)')
            return FirewallState.Keepalive

    except ConnectionError:
        print('ConnectionError - keepalive_func. :(')
        return FirewallState.Fail


def main():
    print("init auth.")

    # read authcred.
    fn = path.expanduser('~/.helloauthcred')  # filename
    with open(fn, 'r') as f:
        (username, password) = [x.strip() for x in f]

    state = FirewallState.Keepalive

    while True:
        if state == FirewallState.Keepalive:
            state = keepalive_func()
            time.sleep(10)
        else:
            state = login_func(username, password)
            time.sleep(10)

        print("state:", state)


if __name__ == "__main__":
    main()
