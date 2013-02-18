#!/usr/bin/env python
# encoding: utf-8
"""
AwardModel.py

Created by Matt Derry on 2013-02-04.
"""

import sys, os, string, sets, math
from noms import *

class AwardModel(object):
    "A class representing the category, winner, show, and presenter of an award"
    def __init__(self, timestamp=None):
        self.category = None
        self.winner = None
        self.presenter = None
        self.score = 0
        self.nominees = []
        self.timestamp = timestamp

    def addNominee(self, nom):
        self.nominees.append(nom)
    
    def removeNominee(self, nom):
        if nom in self.nominees:
            self.nominees.remove(nom)

    def probableNoms(self):
        sortedNoms = sorted(self.nominees, key=lambda nom: nom.score, reverse=True)
        result = []
        i = 0
        while i < min(5,len(sortedNoms)):
            result.append(sortedNoms[i])
            i = i + 1
        return result
            
    
    def printAward(self):
        print "Award: " + self.category
        if self.winner is not None:
            print "\tWinner: " + self.winner.printNom()

    def getKeywords(self):
        words = []
        if self.category is not None:
            s = self.category.translate(string.maketrans("",""), string.punctuation)
            words = s.lower().replace("movie", "motion picture").split()
            if "television" in words:
                indx = words.index("television")
                words[indx] = "tv"
            removeThese = ["best", "the", "in", "a", "or", "made"] # stop-list...
            for r in removeThese:
                if r in words:
                    words.remove(r)
        return words
    
    # compareAwards -- returns 0 if awards deemed to be identical
    def compareAwards(self, award):
        if self.category == award.category:
            return 0
        if self.winner.name == award.winner.name and self.winner.movieOrShow == award.winner.movieOrShow and self.winner.song == award.winner.song:
            return 0
        thesekeys = set(self.getKeywords())
        thosekeys = set(award.getKeywords())
        # check for presence of unique identifiers in keyword lists
        uniqueIDs = ["actor", "actress"]
        for u in uniqueIDs:
            member1 = u in thesekeys
            member2 = u in thosekeys
            if bool(member1) != bool(member2):
                return -1
        maxScore = min(len(thesekeys), len(thosekeys))
        result = maxScore - len(thesekeys.intersection(thosekeys))
        return result
    
    # called on award with a matching category
    def reconcile(self, award):
        if self.winner.movieOrShow is None:
            if award.winner.movieOrShow is not None:
                self.winner.movieOrShow = award.winner.movieOrShow
        else:
            if award.winner.movieOrShow is not None:
                if (award.winner.name != "" and award.winner.name == self.winner.name) or (award.winner.song != "" and self.winner.song == award.winner.song):
                    self.winner.movieOrShow = award.winner.movieOrShow
        if self.winner.name is None:
            if award.winner.name is not None:
                self.winner.name = award.winner.name
        else:
            if award.winner.name is not None:
                if (award.winner.movieOrShow != "" and award.winner.movieOrShow == self.winner.movieOrShow) or (award.winner.song != "" and self.winner.song == award.winner.song):
                    self.winner.name = award.winner.name
        if self.winner.song is None:
            if award.winner.song is not None:
                self.winner.song = award.winner.song
        else:
            if award.winner.song is not None:
                if (award.winner.movieOrShow != "" and award.winner.movieOrShow == self.winner.movieOrShow) or (award.winner.name != "" and award.winner.name == self.winner.name):
                    self.winner.song = award.winner.song
        return

        
    def timeAsString(self):
        return str(self.timestamp.tm_hour) + ":" + str(self.timestamp.tm_min) + ":" + str(self.timestamp.tm_sec)

