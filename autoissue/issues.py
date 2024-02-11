import httpx
import requests
from lxml import etree
from random import randint
import time

NATIONS = []
PASSWORDS = []

URL = 'https://www.nationstates.net/cgi-bin/api.cgi?'

headers = {'User-Agent': 'united_states_of_dictators'}

timeout = httpx.Timeout(90.0, read=None)

for i in range(0, 15):
    nation = f'polithon_{i+1}'
    NATIONS.append(nation)

def issue():
    for n, p in zip(NATIONS, PASSWORDS):
        headers['X-Password'] = p
        response = httpx.get(f'{URL}nation={n}&q=issues', headers=headers, timeout=timeout)
        x_pin = response.headers['X-Pin']
        headers['X-Pin'] = x_pin

        root = etree.fromstring(response.text)

        issues = root.xpath('//ISSUE')
        for issue in issues:
            id = issue.get('id')
            params = {'c': 'issue', 'issue': id, 'option': randint(0, 2)}

            response = httpx.get(f'{URL}nation={n}&q=issues', headers=headers, params=params, timeout=timeout)
            print(response.text)
            print('---------')
            r_remaining = response.headers['RateLimit-Remaining']
            if int(r_remaining) <= 10:
                time.sleep(25)
            time.sleep(5)
issue()
