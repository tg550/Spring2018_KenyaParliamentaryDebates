#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:52:57 2018

@author: guotiankai
"""

import pandas as pd
import glob
import re
import csv

##### set directory by each speaker #####
def Dict(path):
    # a string to record all words
    wordstring =''
    #path = "/Users/guotiankai/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307.txt"
    path = path
    
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
    
    #print(myDict)
    return(myDict)

##### word count(topic) #####
def wordcount_topic(Dict):
    # word count #
    # regular expressions for the words to be counted 
    land = re.compile("land")
    infrastructure=re.compile("infrastructure")
    road=re.compile("road|roads")
    school=re.compile("school|schools")
    hospital=re.compile("hospital|hospitals")
    disease=re.compile("disease")
    corruption=re.compile("corruption")
    economy=re.compile("economy")
    tribe=re.compile("tribe")
    
    headers = ['Speaker','land', 'infrastructure', 'road[s]', 
               'school[s]', 'hospital[s]', 'disease', 'corruption', 'economy', 'tribe', 'word_count']
    
    # Write headers into output CSV file
    with open("wordcount(topic).csv", "w", newline = '', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = headers)
        writer.writeheader()
    
    for key in Dict:
        # a string to record all words
        wordstring =''
        NameSpeaker = key
        wordstring = str(Dict[key])
        wordstring = wordstring.lower()
                
        # using regular expression to find the words and count them
        land_count = str(len(land.findall(wordstring)))
        infrastructure_count = str(len(infrastructure.findall(wordstring)))
        road_count= str(len(road.findall(wordstring)))
        school_count = str(len(school.findall(wordstring)))
        hospital_count = str(len(hospital.findall(wordstring)))
        disease_count = str(len(disease.findall(wordstring)))
        corruption_count= str(len(corruption.findall(wordstring)))
        economy_count = str(len(economy.findall(wordstring)))
        tribe_count=str(len(tribe.findall(wordstring)))
        tokens=wordstring.split()
        n_tokens=len(tokens)
        word_count=n_tokens
        
        # Write the word counts into a CSV file
        with open("wordcount(topic).csv", "a", newline = '', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = headers)
            writer.writerow({'Speaker': str(NameSpeaker),
                             'land':land_count,
                             'infrastructure':infrastructure_count,
                             'road[s]':road_count,
                             'school[s]':school_count,
                             'hospital[s]':hospital_count,
                             'disease':disease_count,
                             'corruption':corruption_count,
                             'economy':economy_count,
                             'tribe':tribe_count,
                             'word_count':word_count})
    



def main():
    # set directory
    myDict = Dict("/Users/guotiankai/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307.txt")
    # calculate word counts
    wordcount_topic(myDict)
    
        
if __name__ == "__main__":   
    main()



