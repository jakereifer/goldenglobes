#!/usr/bin/python

# change above line to point to local 
# python executable

import string, sqlite3 as lite
import re, sys

sql = ["SELECT created_at, tweet FROM tweets WHERE tweet LIKE 'RT @eonline:%' ORDER BY created_at ASC", "SELECT created_at, tweet FROM tweets WHERE tweet LIKE 'RT @goldenglobes:%' ORDER BY created_at ASC"]

strings = ["RT @eonline: Best Supporting Actor in a Drama: Christoph Waltz for Django Unchained! #GoldenGlobes http://t.co/8g8Qsf38",
           "RT @eonline: Best Actor in a TV Series, Drama: Damian Lewis for Homeland #GoldenGlobes http://t.co/mTzTn5TI http://t.co/7YALprfS",
           "RT @eonline: Best TV Series, Drama: Homeland (DUH!) #GoldenGlobes http://t.co/mTzTn5TI",
           "RT @eonline: Best Motion Picture, Drama: Argo! #GoldenGlobes http://t.co/mTzTn5TI (George Clooney AND Ben Affleck on stage? Might be too much handsome.)",
           "RT @eonline: Best Actress in a Motion Picture, Musical or Comedy: Jennifer Lawrence #GoldenGlobes http://t.co/mTzTn5TI",
           "RT @goldenglobes: Best Animated Feature Film - Brave (@PixarBrave) - #GoldenGlobes", "RT @goldenglobes: Best Actress in a Television Series - Drama - Claire Danes - Homeland (@SHO_Homeland) - #GoldenGlobes", "RT @goldenglobes: Best Screenplay - Quentin Tarantino - Django Unchained - #GoldenGlobes", "RT @goldenglobes: Best Foreign Film - Amour (Austria) - #GoldenGlobes", "RT @goldenglobes: Best Supporting Actress in a Motion Picture - Anne Hathaway - Les Miserables - #GoldenGlobes", "RT @goldenglobes: Best Original Score - Mychael Danna - Life of Pi - #GoldenGlobes", "RT @goldenglobes: Best Original Song - \"Skyfall\" - Adele (@OfficialAdele) &amp; Paul Epworth (@PaulEpworth) - Skyfall - #GoldenGlobes"]

# Best Actor in a Motion Picture, Musical or Comedy
# Best Actress in a Motion Picture, Musical or Comedy
# Best Actor in a Miniseries or TV Movie (&)
# Best Actress in a TV Comedy
# Best Television Series Actor - Drama
# Best Original Song


matchObj = re.search(r'RT @\w+: ([Bb]est [\w\s,]*)[:-] (Drama -|Comedy or Musical -|Musical or Comedy)?([A-Za-z\s\"\&-]*)', strings[-1])


    #if matchObj:
    #   print matchObj.groups()
    #   print "rawCat: ", matchObj.group(1)
    #   print "(none): ", matchObj.group(2)
    #   print "rawWinner: ", matchObj.group(3)

con = lite.connect("gg_tweets.sqlite3")

all = []

with con:

    cur = con.cursor()

    for q in sql:
        cur.execute(q)
        rows = cur.fetchall()

        for row in rows:
            result1 = re.search(r'RT @\w+: ([Bb]est [\w\s,]*)[:-] (Drama -|Comedy or Musical -|Musical or Comedy)?([A-Za-z\s\"-]*)(http)?', row[1])
            if result1:
                rawCat = result1.group(1).encode('ascii', 'ignore').strip("- ")
                if result1.group(2) is not None:
                    rawCat = rawCat + " - " + result1.group(2).encode('ascii', 'ignore').strip("- ")
                rawWinner = result1.group(3).encode('ascii', 'ignore').strip("- ")
                if re.search(r'([Dd]ire|[Aa])ct(or|ress)', rawCat) or re.search(r'[Ss]core', rawCat) or re.search(r'[Ss]creenplay', rawCat):
                    result2 = re.search(r'(^[A-Z][A-Za-z-]* [A-Z][A-Za-z-]*( [A-Z][A-Za-z]*)?)(( for| [ -]) (.*))?', rawWinner)
                    if result2:
                        g = result2.groups()
                    else:
                        g = "REGEX ERROR"
                elif re.search(r'\s[Ss]ong', rawCat):
                    result2 = re.search(r'([\"\'\w\s]+) (by|[ -]) ([A-Za-z-]+)?', rawWinner)
                    if result2:
                        g = result2.groups()
                    else:
                        g = "REGEX ERROR"
                else:
                    g = rawWinner
                pair = [rawCat, rawWinner, g]
                if pair not in all:
                    all.append(pair)

indx = 0
for a in all:
    indx = indx+1
    print str(indx) + ":  "  + str(a[0]) + " | " + str(a[1]) + " | "+ str(a[2])

### Done!