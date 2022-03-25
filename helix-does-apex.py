# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:55:28 2021

@author: joshu
"""

import time
import tweepy
import requests
import json
import configparser


global apiKeyHDA, apiSecretHDA, accessHDA, accessSecretHDA
global apiKeyMain, apiSecretMain, accessMain, accessSecretMain
global psnNewDict, psnDict, legendStats  #I'm not sure if these should be global or not?


config = configparser.ConfigParser()
config.read('apexconfig.ini')
apiKeyHDA = config['Keys']['apiKeyHDA']
apiSecretHDA = config['Keys']['apiSecretHDA']
accessHDA = config['Keys']['accessHDA']
accessSecretHDA = config['Keys']['accessSecretHDA']
apiKeyMain = config['Keys']['apiKeyMain']
apiSecretMain = config['Keys']['apiSecretMain']
accessMain = config['Keys']['accessMain']
accessSecretMain = config['Keys']['accessSecretMain']




def newKillCheck(psnNewDict, psnDict):
    """Check for new kills and return # of new kills."""
    #this might need to get refactored to make sense as a function ?
    #this compares the total kills in overview to see if there has been a new kill since previous data was gathered 
    #returns the # of new kills 
    if psnNewDict['data']['segments'][0]['stats']['kills']['displayValue'] != psnDict['data']['segments'][0]['stats']['kills']['displayValue']:
        #set the time.sleep() to a higher number, then update it in this else so it only checks frequently if there is new data coming
        #can have a counter go up for enough failed updates in a row to switch back to slow updates
        #might not have to worry about update speed at all?
        
        #we can update this to review each legend's stats to find where the kills are
        #possible issue when a new character is played for the first time, might address that

        newTotalKills = psnNewDict['data']['segments'][0]['stats']['kills']['displayValue']
        print("New total kills: " + newTotalKills)
        oldTotalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']
        freshKills = str(int(newTotalKills) - int(oldTotalKills))
        psnDict = psnNewDict
        #except for error tweepy.error.TweepError: [{'code': 187, 'message': 'Status is a duplicate.'}]
        
        return freshKills  #this seems to be a string
    else:
        freshKills = "0"  #making this a string to match other freshKills return, idk if it matters
        return freshKills
    
    
def legendSort(data):
    """Return a dictionary of character: stats."""
    sortedDict = {}
    for i in range(len(data['data']['segments'])):
        if i == 0:
            #this skips the overview segment straight to the sortedDict since it doesnt have an id
            sortedDict['overview'] = data['data']['segments'][0]
            continue
        currentLegendData = data['data']['segments'][i]
        currentLegendID = data['data']['segments'][i]['attributes']['id'][-2:] 
            #this gets the last 2 chars of the ID, which will be ## or _#
        currentLegendName = data['data']['segments'][i]['metadata']['name']
        if currentLegendID[0] == '_':
            currentLegendID = currentLegendID[-1:]
            #legend ID seems to be the # order the chars were added
            #ID <10 are _#, this removes the _ so currentLegendID will just be numerical
        print(f"Legend {currentLegendID}: {currentLegendName}")
        sortedDict[currentLegendName] = currentLegendData
        print(f"saved {currentLegendName} to dict")
    #print(sortedDict)
    return sortedDict


def getUpdate():
    """Fetch & return a dictionary with up to date stats."""
    #this could be modified to accept username/platform to look up other users
    print("grabbing update")
    psnNew = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/psn/otherjosh', headers=headers) 
    psnNewDict = psnNew.json()
    return psnNewDict


def sendTweet(freshKills):  #refactor this to work with readableDict to include legend name
    """Send a Tweet based on # of new kills."""
    try:
        if int(freshKills) >= 3:
            api.update_status(f"Big dam! {freshKills} new Apex kills")
            print(f"Big dam! {freshKills} new Apex kills")
        else:
            api.update_status(f"{freshKills} new Apex kills")  #make this have different text for different kill counts
            print(f"{freshKills} new Apex kills")
        #psnDict = psnNewDict
    except tweepy.TweepError as e:
        print(e.reason)
            
            
def readableDict(sortedDict):
    """Remove unneccesary data from sortedDict."""
    badStats = ['percentile', 'displayName', 'displayCategory', 'category', 'metadata', 'displayValue', 'displayType']
    dictKeys = sortedDict.keys()
    #for i in range(len(sortedDict)):  #this goes over each legend
    for key in dictKeys:
        if key == 'overview':
            pass
        for tracker in sortedDict[key]["stats"]:  #this goes over each tracked stat for current legend
            #this caused a key error for "stats" when using data other than my own
            for stat in badStats:
                del sortedDict[key]["stats"][tracker][stat]
    return sortedDict


def findKills(freshKills, prevData, newData):  #might need new/old dict or fresh kills as argument 
    foundKillsDict = {}
    foundKills = 0
    if freshKills != 0:
        for key, value in newData:
            if newData[key] == prevData[key]:
                pass
            else:  
                #this should return a dict with legend: new kills 
                newKills = value['stats']['kills']['value'] - prevData[key]['stats']['kills']['value']
                foundKillsDict[key] = [newKills]
                foundKills += newKills
        if foundKills == freshKills:
            return foundKillsDict
    else:
        pass
        

def log(logData):  #should probably save data after it goes through readableDict
    """Save current data to file."""
    with open('data.json', 'w') as fp:
        json.dump(logData, fp, indent=4)
   

prevData = {}
def loadData():
    """Load previous data."""
    global prevData
    with open('data.json', 'r') as fp:
        prevData = json.load(fp)
        



#runtime ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Twitter stuff:
auth = tweepy.OAuthHandler(apiKeyHDA, apiSecretHDA)
auth.set_access_token(accessHDA, accessSecretHDA)
api = tweepy.API(auth, wait_on_rate_limit=(True), wait_on_rate_limit_notify=(True))
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print("failed to get request token")

#Apex API stuff:
headers = {"TRN-Api-Key":"dbcdc543-8f0c-41f4-9f5e-8e3fb49c2ff0"}
psn = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/psn/otherjosh', headers=headers) 
psnDict = psn.json()
legendStats = legendSort(psnDict)
#legendStats['legendName'] will give all stats for a selected legend or 'overview' json segment

loadData()

#this is basically debug text at this point, but could be modified to be a function or worth keeping
print("old total kills: " + str(psnDict['data']['segments'][0]['stats']['kills']['displayValue']))
totalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']  #this is the total # of kills in list 


#notes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# deleted a psnOld variable, I don't think it was used but could cause errors if so
