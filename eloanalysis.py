# (c) 2017 Charlie Ide
# This file contains modules that I will use to analyze the file containing Elo data

import distancetracker
import sys
import csv
import pickle

def elowin(elo1, elo2):
    '''This function calculates win probability in a game given the elo ratings
    of two teams, using a standard formula from chess.'''
    m=(elo1-elo2)/400
    prob=1-(1/(1+(10**m)))
    return prob

def eloreader(game,team):
    '''This function takes a team and the game # in the season,
    and returns the entry in the Elo database for that game'''
    db=distancetracker.readDB('1314elo.csv')
    for entry in db:
            if entry[6]==str(game):
                if entry[9]==team:
                    return entry

def findcopy(game,team):
    '''This function finds and returns the copy of the game specified in eloreader. 
    I used this to determine what the game number for the opposing
    team was so that I could identify how far they had traveled in the past week'''
    gm=eloreader(game,team)
    db=distancetracker.readDB('1314elo.csv')
    for line in db:
        if line[0]==gm[0]:
            if line[3] !=gm[3]:
                return line
            

def namechanger(name):
    '''Used to make databases compatible with each other'''
    if name=='Hawks':
        return 'atlanta-hawks'
    if name=='Celtics':
        return 'boston-celtics'
    if name=='Nets':
        return 'new-jersey-nets'
    if name=='Bulls':
        return 'chicago-bulls'
    if name == 'Hornets':
        return 'charlotte-bobcats'
    if name=='Cavaliers':
        return 'cleveland-cavaliers'
    if name =='Mavericks':
        return 'dallas-mavericks'
    if name == 'Nuggets':
        return 'denver-nuggets'
    if name == 'Pistons':
        return 'detroit-pistons'
    if name == 'Warriors':
        return 'golden-state-warriors'
    if name == 'Rockets':
        return 'houston-rockets'
    if name == 'Pacers':
        return 'indiana-pacers'
    if name == 'Clippers':
        return 'los-angeles-clippers'
    if name == 'Lakers':
        return 'los-angeles-lakers'
    if name == 'Grizzlies':
        return 'memphis-grizzlies'
    if name == 'Heat':
        return 'miami-heat'
    if name =='Bucks':
        return 'milwaukee-bucks'
    if name == 'Timberwolves':
        return 'minnesota-timberwolves'
    if name == 'Pelicans':
        return 'new-orleans-hornets'
    if name == 'Knicks':
        return 'new-york-knicks'
    if name == 'Thunder':
        return 'oklahoma-city-thunder'
    if name == 'Magic':
        return 'orlando-magic'
    if name == 'Sixers':
        return 'philadelphia-76ers'
    if name=='Suns':
        return 'phoenix-suns'
    if name =='Trailblazers':
        return 'portland-trail-blazers'
    if name == 'Kings':
        return 'sacramento-kings'
    if name == 'Spurs':
        return 'san-antonio-spurs'
    if name == 'Raptors':
        return 'toronto-raptors'
    if name == 'Jazz':
        return 'utah-jazz'
    if name == 'Wizards':
        return 'washington-wizards'

def eloadjuster(game,team):
    '''Given a team and a game, returns the Elo ratings for both teams
    adjusted based on their recent schedules'''
    gm=eloreader(game,team)
    copy=findcopy(game,team)
    opponent=gm[15]
    elo1=float(gm[11])
    elo2=float(gm[17])
    mytm='{}.csv'.format(namechanger(team))
    othertm='{}.csv'.format(namechanger(opponent))
    if gm[19]=='H':
        elo1+=92
    else:
        elo2+=92    
    mytrav=distancetracker.weektrav(int(gm[6]),mytm)
    opponenttrav=distancetracker.weektrav(int(copy[6]),othertm)
    elo1-=(6*(mytrav/1000))
    elo2-=(6*(opponenttrav/1000))
    if distancetracker.prevnight(int(gm[6]),mytm):
        elo1-=46
    if distancetracker.prevnight(int(copy[6]),othertm):
        elo2-=46
    return[elo1,elo2]

def notravadjuster(game,team):
    '''Adjusts elo for home court advantage but not travel, 
    used to determine whether a team benefited or was hurt by their 
    travel schedule and their opponent's travel schedule over the course of the season.
    I use this function in the seasontotals module later.'''
    gm=eloreader(game,team)
    copy=findcopy(game,team)
    opponent=gm[15]
    elo1=float(gm[11])
    elo2=float(gm[17])
    mytm='{}.csv'.format(namechanger(team))
    othertm='{}.csv'.format(namechanger(opponent))
    if gm[19]=='H':
        elo1+=92
    else:
        elo2+=92
    return[elo1,elo2]

def notravwinprob(game,team):
    '''Finds a team's win probability for a game if Elo is only adjusted for home 
    court advantage. Used in seasontotals module to find the net benefit or 
    loss a team receives from their schedule.'''
    elos=notravadjuster(game,team)
    myteam=team
    gm=eloreader(game,team)
    opponent=gm[15]
    regelo1=gm[11]
    regelo2=gm[17]
    myelo=elos[0]
    theirelo=elos[1]
    prob=elowin(myelo,theirelo)
    return prob

def winprob(game,team):
    '''Given a game number and team, returns that team's probability of winning the game
    based on their adjusted elo and their opponent's adjusted elo'''
    elos=eloadjuster(game,team)
    myteam=team
    gm=eloreader(game,team)
    opponent=gm[15]
    regelo1=gm[11]
    regelo2=gm[17]
    myelo=elos[0]
    theirelo=elos[1]
    prob=elowin(myelo,theirelo)
    print("The {} have a {} probability of beating the {}. The {} have an unadjusted elo of {} and an adjusted elo of {}, a net change of {}. The {} have an unadjusted elo of {} and an adjusted elo of {}, a net change of {}.".format(myteam,prob,opponent,myteam,regelo1,myelo,str(float(myelo)-float(regelo1)),opponent,regelo2,theirelo,str(float(theirelo)-float(regelo2))))

def probability(game,team):
    '''Does exactly what the above function does but without the print statement, 
    used in the seasontotals module.'''
    elos=eloadjuster(game,team)
    myelo=elos[0]
    theirelo=elos[1]
    return elowin(myelo,theirelo)
