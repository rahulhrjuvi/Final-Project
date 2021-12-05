# Milestone 2 Part D vocabulary_size_postgres.py

###################### import required packages ######################

import sys
import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg2

###################### defined functions ######################

#repeating the same three defined funcitons in Milestone 2 Part C: preprocess(), ceil_dt(), current_text_fnc()
def preprocess(tweet):
    # remove links
    tweet = re.sub(r'http\S+', '', tweet)
    # remove mentions
    tweet = re.sub("@\w+","",tweet)
    # alphanumeric and hashtags
    tweet = re.sub("[^a-zA-Z#]"," ",tweet)
    # remove multiple spaces
    tweet = re.sub("\s+"," ",tweet)
    tweet = tweet.lower()
    return tweet

def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

def current_text_fnc(text, start_of_current, end_of_current):
    current_text = []
    for i in range(len(text)):
        if time_lst[i]>=start_of_current and time_lst[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

#define function for vocabulary size
def vocabulary_size(text):
    #get a list of processed words.
    tweets_string = ' '.join(text) 
    tweets_string = preprocess(tweets_string)
    tweet_words = tweets_string.split(' ')
    tweet_words = list(filter(lambda a: a != '', tweet_words))
    tweet_words = [item for item in tweet_words if item[0] != '#']
    tweet_words_set = set(tweet_words)
    words_set = len(tweet_words_set)
    
    phrase_list = []
    for i in range(len(tweet_words)-1):
        phrase_list.append(tweet_words[i:i+2])
    phrase_list_set = set(tuple(x) for x in phrase_list)
    phrases = len(phrase_list)-len(text)+1
    phrases_set = len(phrase_list_set)-len(text)+1
    
    uniq_count = words_set+phrases_set

    return uniq_count

#define function for storing each record in schema table unique_words_current_count
def insert_value(insert_query_values):
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()              
    query = """INSERT INTO unique_words_current_count (start_of_current_minute,t,uniq_wph_current_count)
VALUES (%s,%s,%s)"""           
    cursor.execute(query, insert_query_values)
    connection.commit()           
    if connection:
        cursor.close()
        connection.close()

###################### main part ######################

conn = psycopg2.connect(database="final_project", user="gb760")
cur = conn.cursor()
query = """select time_stamp from tweets order by 1 desc limit 1;"""
cur.execute(query)
tm = cur.fetchall()
cur.close()
conn.close()

t = tm[0][0]
start_of_current = ceil_dt(t, timedelta(minutes=-1)) 
end_of_current = t

conn = psycopg2.connect(database="final_project", user="gb760")
cur = conn.cursor()
query = "select * from tweets where time_stamp>='"+str(start_of_current)+"' and time_stamp<='"+str(end_of_current)+"';"
cur.execute(query)
tweets = cur.fetchall()
cur.close()
conn.close()

time_lst = [tweets[x][1] for x in range(len(tweets))]
text_lst = [tweets[x][2] for x in range(len(tweets))]

#get and print the number of unique words used in the tweets posted in the current minute at t
current_text = current_text_fnc(text_lst, start_of_current, end_of_current)
unique_word_count = vocabulary_size(current_text)
print("The number of unique words used in the tweets posted in the current minute", str(start_of_current), "at time t", str(t), "is", unique_word_count, "!")

# insert values into unique_words_current_count table
insert_query_values = (start_of_current,t,unique_word_count)
insert_value(insert_query_values)
print('Insertion into table done!')
