#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:52:57 2018

@author: guotiankai
"""

import pandas as pd
import glob
import re

# a string to record all words
wordstring =''
path = "/Users/guotiankai/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307.txt"
#path = "/Users/guotiankai/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307change.txt"

# read the two files under the folder 1963
read_files = glob.glob(path)

# add them to the wordstring
for f in read_files:
    with open(f, "rb") as infile:
        wordstring+=str(infile.read())

wordstring = wordstring.lower()

#split to paragraph
text   = wordstring.split("\\r\\n")

#create and get dictionary
myDict = dict()
for line in text:
  match = re.search('(.+?):(.*)', line)
  if match: 
    tag, gene = match.groups()
    if tag not in myDict:
        myDict[tag] = gene
    else:
        myDict[tag] += gene

print(myDict)
