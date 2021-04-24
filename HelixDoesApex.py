# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:55:28 2021

@author: joshu
"""

import time
import tweepy
import requests


global apiKeyHDA, apiSecretHDA, accessHDA, accessSecretHDA
global apiKeyMain, apiSecretMain, accessMain, accessSecretMain
    
apiKeyHDA = "ZgBem8FwkI0SHIsQ2xtoYg406"
apiSecretHDA = "sIyiZxVtM5CUINPOphaOApYhIP8GQySesiTGnO5Ke7ss4YsHlj"
accessHDA = "1384162485582786569-jtl8haCB7NdrHR2mEjhNt7VVcONrdg"
accessSecretHDA = "3S2cslhplCXndrDQeoIsznwu0PNxcxhyzscGU2RmfETfr"
    
apiKeyMain = "IRs5nTMGzlZTifbqjFt46l51A"
apiSecretMain = "HlEPVLf47bWlYjnBErtVBAk3SdefaBcUHbCHn1mK1aLLsrrlCd"
accessMain = "4330479552-gCpVIFhh89iZ2z5Ya8x8IyW8v28db0UQrpJujc1"
accessSecretMain = "W4eIfAw9tzeUHDqpFYsAc5Gk02yd8iXc9u47wSNPPBEfm"


auth = tweepy.OAuthHandler(apiKeyHDA, apiSecretHDA)
auth.set_access_token(accessHDA, accessSecretHDA)
api = tweepy.API(auth, wait_on_rate_limit=(True), wait_on_rate_limit_notify=(True))
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print("failed to get request token")


# timeline = api.home_timeline()
# for tweet in timeline:
#     print(f"{tweet.user.name} said {tweet.text}")

#this snippet makes a tweet: 
#api.update_status("Test tweet from tweepy")


#--------------APEX API Stuff-------------------------------------------------
#TRN-Api-Key: #TRN-Api-Key: dbcdc543-8f0c-41f4-9f5e-8e3fb49c2ff0
#origin = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/origin/{platformUserIdentifier}', headers=headers)


headers = {"TRN-Api-Key":"dbcdc543-8f0c-41f4-9f5e-8e3fb49c2ff0"}
psn = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/psn/otherjosh', headers=headers) 
psnDict = psn.json()
print("old total kills: " + str(psnDict['data']['segments'][0]['stats']['kills']['displayValue']))
psnOld = ''

totalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']  #this is the total # of kills in list 
#  legend = psnDict['data']['segments'][1]['metadata']['name']  #this gets legend name 
#  psnDict['data']['segments'][1]['stats']['kills']['displayValue'] also shows # of kills for most recently played chahr 
while True:
    time.sleep(60)  #this waits 10 minutes 
    print("grabbing update")
    psnNew = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/psn/otherjosh', headers=headers) 
    psnNewDict = psnNew.json()
    
    if psnNewDict['data']['segments'][0]['stats']['kills']['displayValue'] == psnDict['data']['segments'][0]['stats']['kills']['displayValue']:
        print("pass")
        pass
    else:
        #set the time.sleep() to a higher number, then update it in this else so it only checks frequently if there is new data coming
        #can have a counter go up for enough failed updates in a row to switch back to slow updates
        print("entered else")
        newTotalKills = psnNewDict['data']['segments'][0]['stats']['kills']['displayValue']
        print("New total kills: " + newTotalKills)
        oldTotalKills = psnDict['data']['segments'][0]['stats']['kills']['displayValue']
        freshKills = str(int(newTotalKills) - int(oldTotalKills))
        api.update_status(f"{freshKills} new Apex kills")
        print(f"{freshKills} new Apex kills")
        psnDict = psnNewDict
        break
    



#while True:  #this feels a lil sketch
    #assign old data to old variable 
    #get new data
    #compare kills 
    #tweet can vary in copy with different ranges of kill 


# Since the order of characters in the json is based on play order, 
# it may be worthwhile to iterate over it and 
# save each character's stats to their own variable - stretch goal 