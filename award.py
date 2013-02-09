#!/usr/bin/env python
# encoding: utf-8
"""
AwardModel.py

Created by Matt Derry on 2013-02-04.
"""

import sys
import os
import string

class AwardModel(object):
   "A class representing the category, winner, show, and presenter of an award"
   def __init__(self, category=None, winner=None, show=None, presenter=None):
      self.category = category
      self.winner = winner
      self.show = show
      self.presenter = presenter
      self.score = 0

   def __str__(self):
      return "Score [%d]: %s goes to %s for %s, presented by %s." % (self.score, self.category.encode('ascii', 'ignore').strip() if self.category is not None else self.category, self.winner.encode('ascii', 'ignore').strip() if self.winner is not None else self.winner, self.show.encode('ascii', 'ignore').strip() if self.show is not None else self.show, self.presenter.encode('ascii', 'ignore').strip() if self.presenter is not None else self.presenter) 

   def length(self):
      length = 0
      if self.category is not None:
         length = length + 1
      if self.show is not None:
         length = length + 1
      if self.presenter is not None:
         length = length + 1
      if self.winner is not None:
         length = length + 1

      return length

   def compareAwards(self, award):
      similarity = 0
      if self.category is not None and award.category is not None:
         if self.category.strip().lower() == award.category.strip().lower():
            similarity = similarity + 1

      if self.winner is not None and award.winner is not None:
         if self.winner.strip().lower() == award.winner.strip().lower():
            similarity = similarity + 1

      if self.show is not None and award.show is not None:
         if self.show.strip().lower() == award.show.strip().lower():
            similarity = similarity + 1

      if self.presenter is not None and award.presenter is not None:
         if self.presenter.strip().lower() == award.presenter.strip().lower():
            similarity = similarity + 1

      return similarity