#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:52:57 2018

@author: guotiankai
"""

import pandas as pd
import glob



# a string to record all words
wordstring =''
path = "307.txt"

# read the two files under the folder 1963
read_files = glob.glob(path)

# add them to the wordstring
for f in read_files:
    with open(f, "rb") as infile:
        wordstring+=str(infile.read())

wordstring = wordstring.lower()