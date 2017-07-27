import json
from urllib import request

import requests

from config import tokenKeys


def isLive(chanID):
    urlRequest = requests.get('https://www.googleapis.com/youtube/v3/search',
                              params={'part': 'snippet',
                                   'channelId': chanID,
                                   'type': 'video',
                                   'eventType': 'live',
                                   'key': tokenKeys.google})
    parsedData = urlRequest.json()
    print(parsedData)
    try:
        title = parsedData['items'][0]['snippet']['title']
        liveLink = parsedData['items'][0]['id']['videoId']
        try:
            thumbnailURL = parsedData['items'][0]['snippet']['thumbnails']['high']['url']
            request.urlretrieve(thumbnailURL, 'thumbnails/' + chanID + 'temp.jpg')
            setThumb = True
        except:
            print('failed at retrieving thumbnail')
            setThumb = False
        chanName = parsedData['items'][0]['snippet']['channelTitle']
        tupleData = (chanID, title, liveLink, chanName, setThumb)
        return tupleData
    except:
        #print('Not Live!')
        return False

#isLive('UCxEGkCtjJ77zoaKqW7ZY97g')

def findLiveChans(cdList):
    calls = 0
    channels = []
    with open('config/serverYTSetup') as jsonOpen:
        jsonData = json.load(jsonOpen)
    tmpChan = []
    gotChan = []
    chanData = []
    for channel in jsonData:
        chanList = jsonData[channel]
        for ytChan in chanList:
            if ytChan in cdList:
                tmpChan.append((channel, ytChan))
    for plzCheck in tmpChan:
        if plzCheck[1] not in gotChan:
            gotChan.append(plzCheck[1])
            data = isLive(plzCheck[1])
            calls+=1
            if data:
                chanData.append(data)
    for getTup in tmpChan:
        for getData in chanData:
            if getTup[1] == getData[0]:
                channels.append((getTup[0], getData))
            #if ytChan not in cdList:
            #    data = isLive(ytChan)
            #    if data:
            #        channels.append((channel, data))
    print(calls)
    return channels

def doesChanExist(chanID):
    urlRequest= requests.get('https://www.googleapis.com/youtube/v3/search',
                             params={'part' : 'snippet',
                                    'channelId': chanID,
                                    'type': 'channel',
                                     'key': tokenKeys.google})
    parsedData = urlRequest.json()
    try:
        print(parsedData['items'][0]['snippet']['title'])
        return True
    except:
        print('Not a Channel')
        return False
