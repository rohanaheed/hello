import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
#import requests
class Resturents:

    BASE_URL = 'https://admin-dev.chowmill.com/api/v1/orders_ratings'
    BASE_URL1='https://admin-dev.chowmill.com/api/v1/restaurants_cuisines'
    HEADERS = {
              'access-token':'_DRIz_uzi6vtMa68CpXjdg',
'client':'_9elVhdVFu5WXIZBVYs_1A',
'expiry':'1554904824',
'token-type': 'Bearer',
'uid': 'ammaryasir3011@gmail.com',
'Access-Control-Allow-Origin': '*',
'Accept':'application/json',
'Content-Type': 'application/json',
'Accept-Language': 'en/US',
            }
    #read data and write in csv file realated to rating
    #response = requests.get(url = BASE_URL, headers=HEADERS)
    #data = response.json()
    #output_fil = '../ml-latest-small/rating.csv'
    #csvFile = open(output_fil, 'w')
    #writer = csv.writer(csvFile, delimiter = ';')
    #writer.writerow([data])
    #read data and write in csv file realated to resturents
    #response1 = requests.get(url = BASE_URL1, headers = HEADERS)
    #data1=response1.json()
    #output_file = '../ml-latest-small/res.csv'
    #csvFile = open(output_file,'w')
    #writer = csv.writer(csvFile,delimiter = ';')
   # writer.writerow([data1])
    resID_to_name = {}
    name_to_resID = {}
    ratingsPath = '../ml-latest-small/rating.csv'
    resturentsPath = '../ml-latest-small/res.csv'
    
    def loadResturentsLatestSmall(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.resID_to_name = {}
        self.name_to_resID = {}

        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.resturentsPath, newline='', encoding='ISO-8859-1') as csvfile:
                resReader = csv.reader(csvfile)
                next(resReader)  #Skip header line
                for row in resReader:
                    resID = int(row[0])
                    resName = row[1]
                    self.resID_to_name[resID] = resName
                    self.name_to_resID[resName] = resID

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = int(row[0])
                if (user == userID):
                    resID = int(row[1])
                    rating = float(row[2])
                    userRatings.append((resID, rating))
                    hitUser = True
                if (hitUser and (user != userID)):
                    break

        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                resID = int(row[1])
                ratings[resID] += 1
        rank = 1
        for resID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[resID] = rank
            rank += 1
        return rankings
    
    def getCates(self):
        cates = defaultdict(list)
        cateIDs = {}
        maxCateID = 0
        with open(self.resturentsPath, newline='', encoding='ISO-8859-1') as csvfile:
            resReader = csv.reader(csvfile)
            next(resReader)  #Skip header line
            for row in resReader:
                resID = int(row[0])
                cateList = row[2].split('|')
                cateIDList = []
                for genre in cateList:
                    if cates in cateIDs:
                        cateID = cateIDs[cates]
                    else:
                        cateID = maxCateID
                        cateIDs[cates] = cateID
                        maxCateID += 1
                    cateIDList.append(cateID)
                cates[resID] = cateIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (resID, genreIDList) in cates.items():
            bitfield = [0] * maxCateID
            for cateID in cateIDList:
                bitfield[cateID] = 1
            cates[resID] = bitfield            
        
        return cates
    
    def getYears(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.resturentsPath, newline='', encoding='ISO-8859-1') as csvfile:
            resReader = csv.reader(csvfile)
            next(resReader)
            for row in resReader:
                resID = int(row[0])
                title = row[1]
                m = p.search(title)
                year = m.group(1)
                if year:
                    years[resID] = int(year)
        return years
    
    def getMiseEnScene(self):
        mes = defaultdict(list)
        with open("LLVisualFeatures13K_Log.csv", newline='') as csvfile:
            mesReader = csv.reader(csvfile)
            next(mesReader)
            for row in mesReader:
                resID = int(row[0])
                avgShotLength = float(row[1])
                meanColorVariance = float(row[2])
                stddevColorVariance = float(row[3])
                meanMotion = float(row[4])
                stddevMotion = float(row[5])
                meanLightingKey = float(row[6])
                numShots = float(row[7])
                mes[resID] = [avgShotLength, meanColorVariance, stddevColorVariance,
                   meanMotion, stddevMotion, meanLightingKey, numShots]
        return mes
    
    def getResName(self, resID):
        if resID in self.resID_to_name:
            return self.resID_to_name[resID]
        else:
            return ""
        
    def getResID(self, resName):
        if resName in self.name_to_resID:
            return self.name_to_resID[resName]
        else:
            return 0