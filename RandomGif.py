import requests
import dotenv
import os
from os.path import join,dirname
import json
import random
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dotenv_path = join(dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

APIKEY = os.getenv('TENOR_APIKEY')
TENORURL = os.getenv('TENOR_URL')
WORDSURL = os.getenv('WORDS_API')
basePayload = {'locale':'en_US', 'key': APIKEY}


def getRandomWord():
    headers = {'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com','X-RapidAPI-Key': 'b7c66b4939msh09af9833488f60dp12e3d3jsnf4d3be3325c4'}
    payload = {'random': 'true'}
    res = requests.get(WORDSURL, params=payload, headers=headers, verify=False)
    jsonRes = json.loads(res.content)
    return jsonRes.get('word')


def getPayload(**kwargs):
    payload = basePayload
    payload['q'] = kwargs.get('searchTerm', None)
    payload['limit'] = kwargs.get('limit', None)

    # Gets results starting at position "value". Use a non-zero
    # "next" value returned by API results to get the next set of
    # results. pos is not an index and may be an integer, float, or string
    payload['pos'] = kwargs.get('pos', None)

    # all, wide, standard
    payload['ar_range'] = kwargs.get('ageRange', None)

    # high - G
    # medium - G and PG
    # low - G, PG, and PG-13
    # off - G, PG, PG-13, and R (no nudity)
    payload['contentfilter'] = kwargs.get('contentFilter', None)

    # basic - nanomp4, tinygif, tinymp4, gif, mp4, and nanogif
    # medium - tinygif, gif, and mp4
    payload['media_filter'] = kwargs.get('mediaFilter', None)

    return payload

def getMP4Url(json, limit=0):
    randomNumber = randomIndexFromLimit(limit)
    return json['results'][int(randomNumber)]['media'][0]['mp4']['url']

def getGIFUrl(json, limit=0):
    print(limit)
    randomNumber = randomIndexFromLimit(limit)
    return json['results'][int(randomNumber)]['media'][0]['gif']['url']

def randomIndexFromLimit(limit):
    return random.randint(0, int(limit))

def getGif(endpoint, **kwargs):
    payload = getPayload(searchTerm=kwargs.get('searchTerm', None), limt=kwargs.get('limit', None), ageRange=kwargs.get('ar_range', None), pos=kwargs.get('pos', None), contentFilter=kwargs.get('contentFilter', None), mediaFilter=kwargs.get('mediaFilter', None))

    res = requests.get(TENORURL + endpoint, params=payload, verify=False)
    jsonRes = json.loads(res.content)

    limit = kwargs.get('limit', None)
    if limit:
        return getGIFUrl(jsonRes, limit)
    else:
        return getGIFUrl(jsonRes)

def getRandomWithTerm(searchTerm, limit, ageRange):

    return getGif('random', searchTerm=searchTerm, limit=limit, ageRange=ageRange)

def getRandom(limit, ageRange):
    word = getRandomWord()
    return getGif('random', searchTerm=word, limit=limit, ageRange=ageRange)


if __name__ == '__main__':
    random.seed(random.randrange(sys.maxsize))
    url2 = getRandom(2, 'all')
    print(url2)
