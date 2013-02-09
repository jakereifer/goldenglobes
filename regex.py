#!/usr/bin/env python
# encoding: utf-8
"""
regex.py

Created by Matt Derry on 2013-02-04.
"""

import sys
import os
import string

class regex(object):
   def __init__(self, regexString = None, catIdx = None, winIdx = None, showIdx = None, presIdx = None):
      self.regexString = regexString
      self.catIdx = catIdx
      self.winIdx = winIdx
      self.showIdx = showIdx
      self.presIdx = presIdx



