# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:55:28 2021

@author: joshu
"""

import time
import tweepy
import requests
import json


global apiKeyHDA, apiSecretHDA, accessHDA, accessSecretHDA
global apiKeyMain, apiSecretMain, accessMain, accessSecretMain
global psnNewDict, psnDict  #I'm not sure if these should be global or not?

apiKeyHDA = "ZgBem8FwkI0SHIsQ2xtoYg406"
apiSecretHDA = "sIyiZxVtM5CUINPOphaOApYhIP8GQySesiTGnO5Ke7ss4YsHlj"
accessHDA = "1384162485582786569-jtl8haCB7NdrHR2mEjhNt7VVcONrdg"
accessSecretHDA = "3S2cslhplCXndrDQeoIsznwu0PNxcxhyzscGU2RmfETfr"
    
apiKeyMain = "IRs5nTMGzlZTifbqjFt46l51A"
apiSecretMain = "HlEPVLf47bWlYjnBErtVBAk3SdefaBcUHbCHn1mK1aLLsrrlCd"
accessMain = "4330479552-gCpVIFhh89iZ2z5Ya8x8IyW8v28db0UQrpJujc1"
accessSecretMain = "W4eIfAw9tzeUHDqpFYsAc5Gk02yd8iXc9u47wSNPPBEfm"

#--------------APEX API Stuff-------------------------------------------------
# TRN-Api-Key: #TRN-Api-Key: dbcdc543-8f0c-41f4-9f5e-8e3fb49c2ff0
# origin = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/origin/{platformUserIdentifier}', headers=headers)
# https://apexlegendsapi.com/documentation.php
# Mcbku9Map6AwnltxSx3n

#this snippet makes a tweet: 
#api.update_status("Test tweet from tweepy")


def newKillCheck(psnNewDict, psnDict):
    #this might need to get refactored to make sense as a function ?
    if psnNewDict['data']['segments'][0]['stats']['kills']['displayValue'] == psnDict['data']['segments'][0]['stats']['kills']['displayValue']:
        print("pass")
        pass
    else:
        #set the time.sleep() to a higher number, then update it in this else so it only checks frequently if there is new data coming
        #can have a counter go up for enough failed updates in a row to switch back to slow updates
        #might not have to worry about update speed at all?
        print("entered else")
        newTotalKills = psnNewDict['data']['segments'][0]['stats']['kills']['displayValue']
        print("New total kills: " + newTotalKills)
        oldTotalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']
        freshKills = str(int(newTotalKills) - int(oldTotalKills))
        psnDict = psnNewDict
        #except for error tweepy.error.TweepError: [{'code': 187, 'message': 'Status is a duplicate.'}]
        
        return freshKills
    
    
def legendSort(data):
    sortedDict = {}
    #this is going to sort the legends by legend_ID
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
    print(sortedDict)
    return sortedDict


def getUpdate():
    print("grabbing update")
    psnNew = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/psn/otherjosh', headers=headers) 
    psnNewDict = psnNew.json()
    return psnNewDict


def sendTweet(freshKills):
    #maybe receive a kill different as argument for this
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
    
    
#runtime ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


print("old total kills: " + str(psnDict['data']['segments'][0]['stats']['kills']['displayValue']))
psnOld = ''
totalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']  #this is the total # of kills in list 
legendStats = legendSort(psnDict)
#legendStats['legendName'] will give all stats for a selected legend or 'overview' json segment
