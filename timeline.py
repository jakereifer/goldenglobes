#!/usr/bin/python

# EECS 337 Assignment 1

import time, sys, unicodedata
from award import *
from commentary import *

class timeline(object):
    # class representing timeline of events

    def __init__(self, begin=None, endtime=None, fashion=None, awards=None):
        self.begin = begin
        self.endtime = endtime
        self.fashion = fashion
        self.awards = awards

    def addAward(self, anAward):
        self.awards.append(anAward)
        return
    
    def timeAsString(self, beginOrEnd):
        if beginOrEnd == 0:
            return str(self.begin.tm_hour) + ":" + str(self.begin.tm_min) + ":" + str(self.begin.tm_sec)
        else:
            return str(self.endtime.tm_hour) + ":" + str(self.endtime.tm_min) + ":" + str(self.endtime.tm_sec)
    
    def summary(self):
        print "\nTHE 2013 GOLDEN GLOBE AWARDS -------- 13 January 2013, (" + self.timeAsString(0) + " - " + self.timeAsString(1) + ") ------------\n\n"
        self.printFashionComm()
        for indx in range(len(self.awards)):
            self.printAwardInfo(indx)
        print "\n\nThat's the end of the Show!"

    def printFashionComm(self):
        if self.fashion:
            print "~Red Carpet Commentary~"
            print "Fashion Commentary List length: ", len(self.fashion)
            print "-----------------------------------"

            sortedFashionCommentary = sorted(self.fashion, key=lambda fsh: fsh.pos_score-fsh.neg_score, reverse=True)
            j = 0
            while j < len(sortedFashionCommentary):
                print j, ": ", sortedFashionCommentary[j]
                j = j+1
    
    def printAwardInfo(self, index):
        if index >= len(self.awards):
            print "\n\nError: specified out-of-range award index: " + str(index)
            return
        anAward = self.awards[index]
        if index == 0:
            print "\n\n~Awards~"
        print "\n---- " + anAward.timeAsString() + " -------------------------------------------"
        print "Award Category: " + anAward.category
        # nominee structure needs to say who and for what (pick out picture/show)
        nomstring = ""
        for nom in anAward.probableNoms():
            nomstring = nomstring + "\n\t"
            if nom.song:
                nomstring = nomstring + nom.song + ", by "
            if nom.name:
                nomstring = nomstring + nom.name + " for "
            if nom.movieOrShow:
                nomstring = nomstring + nom.movieOrShow
            else:
                nomstring = nomstring + "Unknown"
        print "Probable Nominees: " + nomstring
        presenter = "Unknown"
                    #print "Presented by: " + presenter
        winner = ""
        if anAward.winner.song:
            winner = anAward.winner.song + ", by "
        if anAward.winner.name:
            winner = winner + anAward.winner.name + " for "
        if anAward.winner.movieOrShow:
            winner = winner + anAward.winner.movieOrShow
        else:
            winner = winner + "Unknown"
        print "Winner: " + winner
    # need to fix list comp below (and implement commentary...)
    #print "Select Commentary:" +
    #["\n\t" + bit for bit in anAward.comments.bits]
        return
