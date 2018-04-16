#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:52:57 2018

@author: guotiankai
"""
import numpy
import scipy
import pandas as pd
import glob
import re
import csv
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

##### set directory by each speaker #####
def Dict(path):
    # a string to record all words
    wordstring =''
    #path = "C:/Users/tk/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307.txt"
    path = path
    
    # read the two files under the folder 1963
    read_files = glob.glob(path)
    
    # add them to the wordstring
    for f in read_files:
        with open(f, "rb") as infile:
            wordstring+=str(infile.read())
    
    wordstring = wordstring.lower()
    
    #split to paragraph
    text   =  wordstring.split("\\r\\n")
    
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
    '''
    # data clean
    #for k in myDict.keys():
    keys = [k for k, v in myDict.items() if len(v) < 500]
    for xvalue in keys:
        del myDict[xvalue]
    '''
    myDict = ' '.join(myDict)
    #print(myDict)
    #return(myDict)
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
    with open("wordcount(topic)_cleaned.csv", "w", newline = '', encoding='utf-8') as f:
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
        with open("wordcount(topic)_cleaned.csv", "a", newline = '', encoding = 'utf-8') as f:
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
### topic modeling ###     
#Latent Dirichlet allocation (LDA) is a topic model that generates topics based on word frequency from a set of documents. LDA is particularly useful for finding reasonably accurate mixtures of topics within a given document set.
   
def topic_modeling(Dict): 
    # Cleaning and Preprocessing
    # Storing the first text element as a string
    first_text = Dict 
    print(first_text)
    print("="*90)
    print(first_text.split(" "))   
    first_text_list = nltk.word_tokenize(first_text)
    #Stopword Removal
    #nltk.download()
    stopwords = nltk.corpus.stopwords.words('english')
    len(stopwords)
    ##To filter out stop words from our tokenized list of words, we can simply use a list comprehension as follows:
    first_text_list_cleaned = [word for word in first_text_list if word.lower() not in stopwords]
    print(first_text_list_cleaned)
    print("="*90)
    print("Length of original list: {0} words\n"
          "Length of list after stopwords removal: {1} words"
          .format(len(first_text_list), len(first_text_list_cleaned)))
    #Stemming and Lemmatization
    lemm = WordNetLemmatizer()
    
    def print_top_words(model, feature_names, n_top_words):
        for index, topic in enumerate(model.components_):
            message = "\nTopic #{}:".format(index)
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
            print(message)
            print("="*70)
    
    class LemmaCountVectorizer(CountVectorizer):
        def build_analyzer(self):
            analyzer = super(LemmaCountVectorizer, self).build_analyzer()
            return lambda doc: (lemm.lemmatize(w) for w in analyzer(doc))
        
    # Storing the entire training text in a list
    mystr = Dict
    text = re.sub("[^\w]", " ",  mystr).split()
    # Calling our overwritten Count vectorizer
    tf_vectorizer = LemmaCountVectorizer(max_df=0.95, 
                                         min_df=2,
                                         stop_words='english',
                                         decode_error='ignore')
    tf = tf_vectorizer.fit_transform(text)
    
    lda = LatentDirichletAllocation(n_components=11, max_iter=5,
                                    learning_method = 'online',
                                    learning_offset = 50.,
                                    random_state = 0)
    lda.fit(tf)
    
    n_top_words = 40
    print("\nTopics in LDA model: ")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
    
    '''
    # Cleaning and Preprocessing
    # Storing the first text element as a string
    first_text = myDict['mr. nthenge']   
    print(first_text)
    print("="*90)
    print(first_text.split(" "))   
    first_text_list = nltk.word_tokenize(first_text)
    #Stopword Removal
    #nltk.download()
    stopwords = nltk.corpus.stopwords.words('english')
    len(stopwords)
    ##To filter out stop words from our tokenized list of words, we can simply use a list comprehension as follows:
    first_text_list_cleaned = [word for word in first_text_list if word.lower() not in stopwords]
    print(first_text_list_cleaned)
    print("="*90)
    print("Length of original list: {0} words\n"
          "Length of list after stopwords removal: {1} words"
          .format(len(first_text_list), len(first_text_list_cleaned)))
    #Stemming and Lemmatization
    lemm = WordNetLemmatizer()
    
    def print_top_words(model, feature_names, n_top_words):
        for index, topic in enumerate(model.components_):
            message = "\nTopic #{}:".format(index)
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
            print(message)
            print("="*70)
    
    class LemmaCountVectorizer(CountVectorizer):
        def build_analyzer(self):
            analyzer = super(LemmaCountVectorizer, self).build_analyzer()
            return lambda doc: (lemm.lemmatize(w) for w in analyzer(doc))
        
    # Storing the entire training text in a list
    mystr = myDict['mr. nthenge']
    
    mystr = myDict['mr. towett']
    
    text = re.sub("[^\w]", " ",  mystr).split()
    # Calling our overwritten Count vectorizer
    tf_vectorizer = LemmaCountVectorizer(max_df=0.95, 
                                         min_df=2,
                                         stop_words='english',
                                         decode_error='ignore')
    tf = tf_vectorizer.fit_transform(text)
    
    lda = LatentDirichletAllocation(n_components=11, max_iter=5,
                                    learning_method = 'online',
                                    learning_offset = 50.,
                                    random_state = 0)
    lda.fit(tf)
    
    n_top_words = 40
    print("\nTopics in LDA model: ")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
    '''



def main():
    # set directory
    myDict = Dict("/Users/guotiankai/Google Drive/Georgetown/Spring2018_4/RA/Spring2018_KenyaParliamentaryDebates/demo_1963Mar12/307.txt")
    # calculate word counts
    wordcount_topic(myDict)
    
        
if __name__ == "__main__":   
    main()



