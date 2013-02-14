#!/usr/bin/python

# EECS 337 Assignment 1

# Nominee class and sub-classes
class nominee(object):
    def __init__(self, movieOrShow=None, name=None, song=None):
        self.movieOrShow = movieOrShow
        self.name = name
        self.song = song

    def printNom(self):
        result = "Nominee: "
        if self.name is not None:
            result = result + " name: " + self.name
        if self.movieOrShow is not None:
            result = result + " Movie or Show: " + self.movieOrShow
        if self.song is not None:
            result = result + " song: " + self.song
        return result