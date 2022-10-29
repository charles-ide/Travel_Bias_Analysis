#This program pulls distances from the website sportsmapworld.com and writes it to the csv file that I created of distances.
# (c) 2017 Charlie Ide

import requests
import re
import time
import pickle

teamList=['atlanta-hawks','boston-celtics','new-jersey-nets','charlotte-bobcats','chicago-bulls','cleveland-cavaliers','dallas-mavericks','denver-nuggets','detroit-pistons','golden-state-warriors','houston-rockets','indiana-pacers','los-angeles-clippers','los-angeles-lakers','memphis-grizzlies','miami-heat','milwaukee-bucks','minnesota-timberwolves','new-orleans-hornets','new-york-knicks','oklahoma-city-thunder','orlando-magic','philadelphia-76ers','phoenix-suns','portland-trail-blazers','sacramento-kings','san-antonio-spurs','toronto-raptors','utah-jazz','washington-wizards']

def distances():
    '''Creates a dictionary of dictionaries containing every team in the NBA, and how far that team must travel to every other team in the NBA, I then saved this dictionary as a pickle file.'''
    
    d=dict()
    for team1 in teamList:
        tempd=dict()
        for team2 in teamList:
            url = 'http://www.sportmapworld.com/distance/{}/{}/'.format(team1,team2)
            while True:
                r=requests.get(url)
                if r.status_code != 200:
                    raise Exception('Invalid request')
                if r.text.find('Error:ORA') == -1:
                    break;
                time.sleep(1)
            t=r.text
            dpat = '<meta name="description" content="Distance between (.*)and(.*)is ([0-9]*)(.*)" />'
            for (tm1,tm2,dist,extra) in re.findall(dpat,t):
                distance=int(dist)
                tempd[team2]=distance
        d[team1]=tempd
    with open('distances.pickle','wb') as handle:
        pickle.dump(d,handle,protocol=pickle.HIGHEST_PROTOCOL)
    
if __name__=='__main__':
    distances()
    
