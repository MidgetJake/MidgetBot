import tokenKeys
import requests
import json
from urllib import request

title = '-Default-'
liveLink = '-Default-'
thumbN = '-Default-'

def isLive(chanID):
    urlRequest = requests.get('https://www.googleapis.com/youtube/v3/search',
                           params={'part': 'snippet',
                                   'channelId': chanID,
                                   'type': 'video',
                                   'eventType': 'live',
                                   'key': tokenKeys.google})
    parsedData = urlRequest.json()
    #print(parsedData)
    try:
        title = parsedData['items'][0]['snippet']['title']
        liveLink = 'http://youtube.com/channel/'+chanID+'/live'
        thumbN = parsedData['items'][0]['snippet']['thumbnails']['high']['url']
        #print(title)
        #print(liveLink)
        #print(thumbN)
        return True
    except:
        #print('Not Live!')
        return False

def findLiveChans(timeCheck):
    channels = []
    if(timeCheck > 5000000):
        with open('serverYTSetup') as jsonOpen:
            jsonData = json.load(jsonOpen)
        for channel in jsonData:
            chanList = jsonData[channel]
            for ytChan in chanList:
                if (isLive(ytChan)):
                    channels.append((channel, ytChan))
    return channels

def getLiveTitle(chanID):
    print('Trying to get Title')
    urlRequest = requests.get('https://www.googleapis.com/youtube/v3/search',
                              params={'part': 'snippet',
                                      'channelId': chanID,
                                      'type': 'video',
                                      'eventType': 'live',
                                      'key': tokenKeys.google})
    parsedData = urlRequest.json()
    return parsedData['items'][0]['snippet']['title']

def getLiveThumbnail(chanID):
    print('Trying to get Thumbnail')
    urlRequest = requests.get('https://www.googleapis.com/youtube/v3/search',
                           params={'part': 'snippet',
                                   'channelId': chanID,
                                   'type': 'video',
                                   'eventType': 'live',
                                   'key': tokenKeys.google})
    parsedData = urlRequest.json()
    try:
        thumbnailURL = parsedData['items'][0]['snippet']['thumbnails']['high']['url']
        request.urlretrieve(thumbnailURL, "temp.jpg")
    except:
        print('Something went wrong getting the thumbnail')

def getLiveLink(chanID):
    print('Trying to get the stream link!')
    urlRequest = requests.get('https://www.googleapis.com/youtube/v3/search',
                           params={'part': 'snippet',
                                   'channelId': chanID,
                                   'type': 'video',
                                   'eventType': 'live',
                                   'key': tokenKeys.google})
    parsedData = urlRequest.json()
    try:
        return parsedData['items'][0]['id']['videoId']
    except:
        print('Something went wrong getting the link')



def getChanName(chanID):
    print('Trying to get the channel name')
    urlRequest= requests.get('https://www.googleapis.com/youtube/v3/search',
                           params={'part' : 'snippet',
                                    'channelId': chanID,
                                    'type': 'channel',
                                     'key': tokenKeys.google})
    parsedData = urlRequest.json()
    return (parsedData['items'][0]['snippet']['title'])

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
