# (c) Charlie Ide 2017
# This file contains functions used to determine how many wins a team gained or lost in a season based
# on their travel schedule and their oppoents travel schedule. It looks at how many wins they would expect if
# travel adjustments are not factored in and how many wins they would expect with travel adjustments and then takes finds the difference
# over the course of the season for each team.

import eloanalysis
import pickle

teamlist=['Hawks','Celtics','Nets','Hornets','Bulls','Cavaliers','Mavericks','Nuggets','Warriors','Rockets','Pistons','Clippers','Grizzlies','Heat','Bucks','Timberwolves','Pelicans','Knicks','Thunder','Magic','Sixers','Suns','Trailblazers','Kings','Lakers','Pacers','Spurs','Raptors','Jazz','Wizards']

def seasonanalysis(team):
    '''Given an NBA team, returns how many wins they gained or lost over the course of the season from their travel schedule.'''
    unadjustedwins=0
    adjustedwins=0
    for i in range(3,83):
        adjustedwins+=eloanalysis.probability(i,team)
    for i in range (2,83):
        unadjustedwins+=eloanalysis.notravwinprob(i,team)

    return adjustedwins-unadjustedwins

def allteamanalysis():
    '''Creates and pickles a dictionary of all teams and how many wins they gain or lose due to travel over the course of the season'''
    d=dict()
    for team in teamlist:
        wins=seasonanalysis(team)
        d[team]=wins
        print(team)
    with open('seasontotals.pickle','wb') as handle:
        pickle.dump(d,handle,protocol=pickle.HIGHEST_PROTOCOL)
    return d
