#!/usr/bin/env python
# encoding: utf-8
"""
commentary.py

Created by Matt Derry on 2013-02-05.
"""

import sys
import os

class FashionCommentaryModel:
	def __init__(self, subject=None, pos_commentary=None, neg_commentary=None):
		self.subject=subject
		self.positive_commentary=pos_commentary
		self.negative_commentary=neg_commentary
		self.pos_score=0
		self.neg_score=0

	def __str__(self):
		if self.pos_score > (5*self.neg_score):
			return "Overall, people really like how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.positive_commentary.encode('ascii', 'ignore').strip() if self.positive_commentary is not None else self.positive_commentary)
		elif self.pos_score > (3*self.neg_score):
			return "Overall, people generally like how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.positive_commentary.encode('ascii', 'ignore').strip() if self.positive_commentary is not None else self.positive_commentary)
		elif self.pos_score > self.neg_score:
			return "Overall, people kind of like how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.positive_commentary.encode('ascii', 'ignore').strip() if self.positive_commentary is not None else self.positive_commentary)
		elif self.pos_score == self.neg_score:
			return "Overall, people were neutral about how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.positive_commentary.encode('ascii', 'ignore').strip() if self.positive_commentary is not None else self.positive_commentary)
		elif (5*self.pos_score) < self.neg_score:
			return "Overall, people hate how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.negative_commentary.encode('ascii', 'ignore').strip() if self.negative_commentary is not None else self.negative_commentary)
		elif (3*self.pos_score) < self.neg_score:
			return "Overall, people generally dislike how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.negative_commentary.encode('ascii', 'ignore').strip() if self.negative_commentary is not None else self.negative_commentary)
		elif self.pos_score < self.neg_score:
			return "Overall, people don't really like how %s looked.\n An example tweet: \"%s\"" % (self.subject.encode('ascii', 'ignore').strip() if self.subject is not None else self.subject, self.negative_commentary.encode('ascii', 'ignore').strip() if self.negative_commentary is not None else self.negative_commentary)
		
	