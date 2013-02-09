#!/usr/bin/python

# change above line to point to local 
# python executable

import string, sqlite3 as lite
import re, sys, unicodedata
from award import *
from regex import *

con = lite.connect('gg_tweets.sqlite3')

awards = []

sqlQueries = ["SELECT tweet FROM tweets WHERE tweet LIKE '%win%' AND tweet NOT LIKE 'RT @%'", "SELECT tweet FROM tweets WHERE tweet LIKE 'RT @eonline:%'"]

rX1 = regex(r'(.*)\bwins (Golden Globe)?(.*)for(.*)', -1, 1, -1, -1)
rX2 = regex(r'RT @eonline: (.*): (.*)for ([a-zA-Z ]*)(!)? (#GoldenGlobes|http://(.*))+(.*)', 1, 2, 3, -1)
rX3 = regex(r'RT @eonline: (Best (Motion|TV)+([a-zA-Z, ]*)): ([a-zA-Z ]*)(.*)(!)?(.*) (#GoldenGlobes|http://(.*))+(.*)', 1, 4, 4, -1)

regexes = [rX1, rX2, rX3]

with con:
   for query in sqlQueries:
      cur = con.cursor()
      cur.execute(query)	
      rows = cur.fetchall()

      for row in rows:
         i = 0
         for regex in regexes:	
            matchObj = re.match(regex.regexString, row[0])

            if matchObj:
               a = AwardModel()
               if regex.catIdx is not None and regex.catIdx > 0:
                  a.category = matchObj.group(regex.catIdx)
               if regex.winIdx is not None and regex.winIdx > 0:
                  a.winner = matchObj.group(regex.winIdx)
               if regex.showIdx is not None and regex.showIdx > 0:
                  a.show = matchObj.group(regex.showIdx)
               if regex.presIdx is not None and regex.presIdx > 0:
                  a.presenter = match.Obj.group(regex.presIdx)

               maxSimilarity = 0
               for award in awards:
                  sim = a.compareAwards(award)

                  if sim == min(a.length(), award.length()):
                     if a.length() > award.length():
                        award.category = a.category
                        award.winner = a.winner
                        award.show = a.show
                        award.presenter = a.presenter
                        sim = a.length()

                  a.score = a.score + sim
                  award.score = award.score + sim
                  if sim > maxSimilarity:
                     maxSimilarity = sim

               if maxSimilarity < a.length():
                  awards.append(a)


print "Awards"
print "Awards List length: ", len(awards)
print "-----------------------------------"

sortedAwards = sorted(awards, key=lambda award: award.score, reverse=True)
j = 0
while j < 30:
   print j, ": ", sortedAwards[j]
   j = j+1

### Done!