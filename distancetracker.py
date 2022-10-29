#This file contains functions that I used to tabulate the distance traveled by an NBA team in the past week
# (c) 2017 Charlie Ide
import csv
import pickle

def readDB(database):
    '''Loads up a team's schedule into a database. The database being loaded corresponds to the csv files I have saved such as boston-celtics.csv'''
    results = []
    with open(database, 'r') as f:
        csvf = csv.reader(f)
        for row in csvf:
            results.append(row)
        return results
        
def parseDate(team):
    '''Converts the date into a parsed list, I used this function for the progress function later'''
    d=dict()
    for line in readDB(team):
            date = line[1]
            date.split(sep=',', maxsplit=1)
            newdate = date.split()
            d[line[0]] = newdate
    return d
    

def progress(game,team):
    '''Given a game, returns how many days have passed since September 30, 2016. This function was used so I could assign a number to each day in the NBA season, this number was very useful to my functions later.'''
    number = parseDate(team)[str(game)]
    month = number[1]
    day=number[2]
    year=number[3]
    prog=0
    if month=='Nov':
        prog+=31
    if month=='Dec':
        prog+=61
    if month=='Jan':
        prog+=92
    if month=='Feb':
        prog+=123
    if month=='Mar':
        prog+=151
    if month=='Apr':
        prog+=182
    prog+=int(day)
    return prog

def prevnight(game,team):
    '''Returns true if a team played a game on the previous night, else returns false'''
    previous=False
    if progress(game,team)-progress(game-1,team)==1:
        previous=True
    return previous


def travel(game, team):
    '''Given the game #, returns the distance the team traveled between the current game and the last game. To do this 
    the program loads and reads the pickled dictionary of dictionaries of distances between teams.'''
    with open('distances.pickle','rb') as handle:
        book=pickle.load(handle)
        DB=readDB(team)
        currentgm=DB[game]
        lastgm=DB[game-1]
        if currentgm[5] == '@':
            if currentgm[6].lower().replace(' ','-')=='charlotte-hornets':
                newlocation='charlotte-bobcats'
            elif currentgm[6].lower().replace(' ','-') == 'brooklyn-nets':
                newlocation='new-jersey-nets'
            elif currentgm[6].lower().replace(' ','-')=='new-orleans-pelicans':
                newlocation='new-orleans-hornets'
            else:
                newlocation = currentgm[6].lower().replace(' ','-')
        else:
            newlocation = 'boston-celtics'
        if lastgm[5] == '@':
            if lastgm[6].lower().replace(' ','-')=='charlotte-hornets':
                 oldlocation='charlotte-bobcats'
            elif lastgm[6].lower().replace(' ','-')=='brooklyn-nets':
                oldlocation='new-jersey-nets'
            elif lastgm[6].lower().replace(' ','-')=='new-orleans-pelicans':
                oldlocation='new-orleans-hornets'
            else:
                oldlocation = lastgm[6].lower().replace(' ','-')
        else:
            oldlocation = 'boston-celtics'
        distance=book[oldlocation][newlocation]
        return distance

def weektrav(game, team):
    '''Given a game number during the season, returns how many miles the team has traveled during the 
    past week'''
    prog=progress(game,team)
    count=progress(game,team)
    trav=0
    number=game
    while prog>=(count-6):
        if number==1:
            trav+=0
            break
        else:    
            trav+=travel(number,team)
            number-=1
            prog=progress(number,team)
    return trav
