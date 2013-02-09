#!/usr/bin/python

# change above line to point to local 
# python executable

import string, sqlite3 as lite
import re, sys

strings = ["RT @eonline: Best Supporting Actor in a Drama: Christoph Waltz for Django Unchained! #GoldenGlobes http://t.co/8g8Qsf38",
           "RT @eonline: Best Actor in a TV Series, Drama: Damian Lewis for Homeland #GoldenGlobes http://t.co/mTzTn5TI http://t.co/7YALprfS",
           "RT @eonline: Best TV Series, Drama: Homeland (DUH!) #GoldenGlobes http://t.co/mTzTn5TI",
           "RT @eonline: Best Motion Picture, Drama: Argo! #GoldenGlobes http://t.co/mTzTn5TI (George Clooney AND Ben Affleck on stage? Might be too much handsome.)",
           "RT @eonline: Best Actress in a Motion Picture, Musical or Comedy: Jennifer Lawrence #GoldenGlobes http://t.co/mTzTn5TI"]

matchObj = re.match( r'RT @eonline: (.*): (.*)for ([a-zA-Z ]*)(!)? (#GoldenGlobes|http://(.*))+(.*)', strings[4])

if matchObj:
   print matchObj.groups()
   print "Category: ", matchObj.group(1)
   print "Winner: ", matchObj.group(2)
   print "Show: ", matchObj.group(3)

### Done!