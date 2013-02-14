#!/usr/bin/python

# EECS 337 Assignment 1

import sqlite3 as lite
import re, time
from timeline import *
from award import *
from noms import *
from commentary import *
from regex import *

# queries to get beginning and end time of the event
sql_get_begEnd = ["SELECT created_at FROM tweets ORDER BY created_at ASC LIMIT 0,1", "SELECT created_at FROM tweets ORDER BY created_at DESC LIMIT 0,1"]

# awards queries -- retrieve database records in chronological order
sql_init = ["SELECT created_at, tweet FROM tweets WHERE tweet LIKE 'RT @eonline:%' ORDER BY created_at ASC", "SELECT created_at, tweet FROM tweets WHERE tweet LIKE 'RT @goldenglobes:%' ORDER BY created_at ASC"]

sql_all_tweets = "SELECT tweet FROM tweets"

# regexes for fashion commentary
rX1 = regex(r'([a-zA-Z]* [a-zA-Z\']*)? looks (so |really |absolutely )?(fantastic|amazing|wonderful|fabulous|great|good|stunning|ravishing|beautiful|sensational|hot|sexy|gorgeous|effortless|awesome|ethereal|effervescent|radiant|fierce|lovely|elegant|flawless|divine|pretty|cute|incredible)+(.*)')
rX2 = regex(r'([a-zA-Z]* [a-zA-Z\']*)? (looks|is) (so |really |absolutely )?(horrible|ugly|gross|terrible|horrendous|attrocious|fat|cheap|slutty|busted|unflattering|ill-fitting|old|heavy|missed the mark|like a distaster|awful|messy|hot mess|a mess[. !,]|dreadful|horrid|appalling){1}(.*)')
regexes = [rX1, rX2]

# Exmaple tweet formats:
# RT @eonline: Best Original Song, Motion Picture: Skyfall by @OfficialAdele! #GoldenGlobes (url) (url)
# RT @goldenglobes: Best Supporting Actor in a Motion Picture - Christoph Waltz - Django Unchained - #GoldenGlobes   

con = lite.connect("gg_tweets.sqlite3")

timeInterval = ["",""]
fashion = []
awards = []

with con:
    cur = con.cursor()
    
    for q in range(len(sql_get_begEnd)):
        cur.execute(sql_get_begEnd[q])
        row = cur.fetchone()
        timeInterval[q] = re.search(r'\s([\w:]+)', str(row[0])).group(1).encode('ascii', 'ignore')
        
    eventTimeline = timeline(timeInterval[0],timeInterval[1])

    # commence query process for fashion commentary
    cur.execute(sql_all_tweets)
    rows = cur.fetchall()
    for row in rows:
        i = 0
        for regex in regexes:
            matchObj = re.match(regex.regexString, row[0])
        
            if matchObj:
                f = FashionCommentaryModel()
                f.subject = matchObj.group(1)
                if i == 0:
                    f.positive_commentary = matchObj.group(0)
                else:
                    f.negative_commentary = matchObj.group(0)
            
                foundSubject = 0
                for fsh in fashion:
                    if fsh.subject.lower() == f.subject.lower():
                        foundSubject = 1
                        if i == 0:
                            fsh.pos_score = fsh.pos_score + 1
                        else:
                            fsh.neg_score = fsh.neg_score + 1
            
                if foundSubject == 0:
                    if i == 0:
                        f.pos_score = 1
                    else:
                        f.neg_score = 1
                    fashion.append(f)
            i = i+1

    eventTimeline.fashion = fashion

    # commence querying for award cats/winners
    for query in sql_init:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            # RT from @eonline or @goldenglobes
            result1 = re.search(r'RT @\w+: ([Bb]est [\w\s,]*)[:-] (Drama -|Comedy or Musical -|Musical or Comedy)?([A-Za-z\s\"-]*)(http)?', row[1])
            if result1:
                    
                # get timestamp
                tStamp = re.search(r'\s([\w:]+)', str(row[0])).group(1).encode('ascii', 'ignore')
                    
                # get raw data
                rawCat = result1.group(1).encode('ascii', 'ignore').strip("- ")
                if result1.group(2) is not None:
                    rawCat = rawCat + " - " + result1.group(2).encode('ascii', 'ignore').strip("- ")
                rawWinner = result1.group(3).encode('ascii', 'ignore').strip("- ")

                # initialize award and nominee
                tmpAward = AwardModel(tStamp)
                tmpNom = nominee()
                tmpAward.category = rawCat
                
                # winner string at this point includes invidual(s) or song and movie
                if re.search(r'([Dd]ire|[Aa])ct(or|ress)', rawCat) or re.search(r'[Ss]core', rawCat) or re.search(r'[Ss]creenplay', rawCat):
                    result2 = re.search(r'(^[A-Z][A-Za-z-]* [A-Z][A-Za-z-]*( [A-Z][A-Za-z]*)?)(( for| [ -]) (.*))?', rawWinner)
                    if result2:
                        tmpNom.name = result2.group(1).encode('ascii', 'ignore').strip("- ")
                        if result2.group(5) is not None:
                            tmpNom.movieOrShow = result2.group(5).strip("- ")
                    #else:
                        #print "REGEX ERROR (1)"
                # song award(s)
                elif re.search(r'\s[Ss]ong', rawCat):
                    result2 = re.search(r'([\"\'\w\s]+) (by|[ -]) ([A-Za-z-]+)?', rawWinner)
                    if result2:
                        tmpNom.song = result2.group(1).strip("-\"\' ")
                        tmpNom.movieOrShow = tmpNom.song # hacky...
                        if result2.group(3):
                            tmpNom.name = result2.group(3).strip("-\"\' ")
                    #else:
                        #print "REGEX ERROR (2)"
                # generic awards - movies rather than individuals
                else:
                    tmpNom.movieOrShow = rawWinner

                tmpAward.winner = tmpNom
                tmpAward.addNominee(tmpNom)
                        
                found = 0
                count = 0
                while count < len(awards) and found == 0:
                    compareResult = awards[count].compareKeywords(tmpAward)
                    if compareResult == 0:
                        found = 1
                        awards[count].reconcile(tmpAward)
                        awards[count].score = awards[count].score + 1
                    count = count + 1
                if found == 0:
                    awards.append(tmpAward)

eventTimeline.awards = sorted(awards, key=lambda award: award.timestamp)
eventTimeline.summary()
