#!/usr/local/bin/python3

import json
import requests
import datetime
import sys

myKey='AE6F78043D0710C67D324966DEC7C38D'
yySteamID='76561198100561326'
yyAccountID='140295598'

def printPlayerInfo(steamID=yySteamID):
    apiurl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    args = {'steamids': steamID, 'key': myKey}
    url = requests.get(apiurl, params=args).url
    playerInfo = requests.get(url).json()
    nickname = playerInfo['response']['players'][0]['personaname']
    state = playerInfo['response']['players'][0]['personastate']
    lastlogoff = playerInfo['response']['players'][0]['lastlogoff']
    lastlogoff = datetime.datetime.fromtimestamp(lastlogoff).strftime('%Y-%m-%d %H:%M:%S')
    print('--- Player Info ---')
    print('nickname:          ' + nickname)
    print('last log off time: ' + lastlogoff)
    print('current state:     ' + str(state))

def getMostRecentMatch(accountID=yyAccountID):
    apiurl = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/'
    args = {'account_id': accountID, 'key': myKey}
    url = requests.get(apiurl, params=args).url
    MatchesInfo = requests.get(url).json()
    return MatchesInfo['result']['matches'][0]['match_id']

def printMatchDetail(matchID, accountID=yyAccountID):
    apiurl = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1'
    args = {'match_id': matchID, 'key': myKey}
    url = requests.get(apiurl, params=args).url
    MatchDetail = requests.get(url).json()
    print('--- The Latest Match (' + str(matchID) + ') ---')
    for i in range(0,10):
        if MatchDetail['result']['players'][i]['account_id'] == int(accountID):
            kills = MatchDetail['result']['players'][i]['kills']
            deaths = MatchDetail['result']['players'][i]['deaths']
            assists = MatchDetail['result']['players'][i]['assists']
            kda = str(kills) + '/' + str(deaths) + '/' + str(assists)
            goldpermin = str(MatchDetail['result']['players'][i]['gold_per_min'])
            xppermin = str(MatchDetail['result']['players'][i]['xp_per_min'])
            print("K/D/A:    " + kda)
            print("Gold/min: " + goldpermin)
            print("XP/min:   " + xppermin)
            if (MatchDetail['result']['radiant_win'] and 0 <= i <= 4) or (not MatchDetail['result']['radiant_win'] and 5 <= i <= 9):
                print('YY在最新的一场战斗中，以惊人的' + kda + '的KDA，扶大厦之将倾，凭借着每分钟' + goldpermin + '金钱，击败了对面的弱鸡。让我们掌声祝贺！')
            else:
                print('猪队友总是让人憎恨。纵使YY在过去的一场比赛中取得了逆天的' + kda + '的KDA，但终究无法一带四，虽然打出了每分钟' + goldpermin + '的金钱，送给队友四把圣剑，但无力回天。让我们再一次唾骂这些猪队友！')

if __name__ == '__main__':
    printPlayerInfo()
    printMatchDetail(getMostRecentMatch())
