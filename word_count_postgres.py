#!/usr/bin/env python
# coding: utf-8

# Milestone 2 Part C word_count_postgres.py

import argparse
import sys
import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg2


# In[7]:


# Cleaning the tweets
# reference link: https://gist.github.com/aniruddha27/8d112b87ff4014b80f606dc68080066d#file-preprocess_tweets-py
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


# In[14]:


# open a connection (close it later)
conn = psycopg2.connect(database="final_project", user="gb760")
# create a cursor
cur = conn.cursor()
# execute a SQL command
query = """
select * from tweets;
"""
cur.execute(query)

#get the tweets content list - each row of the table tweets is a tuple
tweets_lst = cur.fetchall()


# In[22]:


time_lst = [tweets_rows[1] for tweets_rows in tweets_lst]
text_lst = [tweets_rows[2] for tweets_rows in tweets_lst]


# In[51]:


#In order to have both current and prior tweet texts, 
#our group assume the time t is two minutes after the time we run server_postgres.py, 
#and the time we run the py file is approximately equal to the time of posting the first tweet in our tweets table.

#https://stackoverflow.com/questions/13071384/ceil-a-datetime-to-next-quarter-of-an-hour
def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

t = time_lst[0]+timedelta(minutes = 2)
start_of_current = ceil_dt(t, timedelta(minutes=-1)) 
end_of_current = ceil_dt(t, timedelta(minutes=1)) - timedelta(seconds = 1)
####start_of_prior = ceil_dt(time_lst[0], timedelta(minutes=1))
####end_of_prior = start_of_prior + timedelta(seconds = 59)


# In[52]:


def current_text(text, start_of_current, end_of_current):
    current_text = []
    for i in range(len(text)):
        if time_lst[i]>=start_of_current and time_lst[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

#unprocessed tweet text list of current minute at t
current_text = current_text(text_lst, start_of_current, end_of_current)


# In[126]:


def calculation_numbers(text, my_input):
    #get a list of processed words.
    tweets_string = ' '.join(text) 
    tweets_string = preprocess(tweets_string) #put all processed tweets texts into a single string.
    tweet_words = tweets_string.split(' ') #split the string into a list with space.
    tweet_words = list(filter(lambda a: a != '', tweet_words)) #drop the ''.
    tweet_words = [item for item in tweet_words if item[0] != '#'] #drop the remaining sign '#'.
    #if input is phrase - Consider only the phrases of two words here.
    if ' ' in my_input:
        my_input = my_input.split(' ')
        phrase_list = []
        for i in range(len(tweet_words)-1):
            phrase_list.append(tweet_words[i:i+2]) #a processed list of all the two-word phrases
        count = phrase_list.count(my_input)
        ####phrase_list_set = set(tuple(x) for x in phrase_list)
        return count, len(phrase_list) ####, len(phrase_list_set)
    else:
        ####tweet_words_set = set(tweet_words)
        count = 0
        count += tweets_string.count(my_input)
        return count, len(tweet_words) ####, len(tweet_words_set)

#Parsing functionality
parser = argparse.ArgumentParser(description='Computes Word/Phrase Frequency.')
parser.add_argument("--word", help="Computes Word/Phrase Frequency.", default="")
args = parser.parse_args()
word = args.word
word = word.lower() #transform everything we input to lowercases.
if word == '':
    print ("You need to use <python3 word_count_postgres.py --word 'xxx'> and put the word or phrases you want to compute frequncy in the argument 'xxx'!")
    sys.exit()
print ("Computing Frequency for '",word,"'!" )

#get the no. of times p was seen in the current minute at t and total no. of phrases seen in the current minute at t.
current_p_occurences, current_total_count = calculation_numbers(current_text,word)


# In[124]:


#print the frequency of p in the current minute at t

print("The word/phrase frequency for '", word, "' in the current minute t = ", str(t), "is", current_p_occurences, "!")


# In[128]:


# reset word_current_count table
def reset_word_current_count_table():
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE word_current_count""")
    connection.commit()
    if connection:
        cursor.close()
        connection.close()

reset_word_current_count_table()  


# In[130]:


# insert values into word_current_count table
def insert_value(insert_query_values):
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()              
    query = """INSERT INTO word_current_count (p,t,start_of_current_minute,end_of_current_minute,p_current_freq,total_p_current)
VALUES (%s,%s,%s,%s,%s,%s)"""           
    cursor.execute(query, insert_query_values)
    connection.commit()           
    if connection:
        cursor.close()
        connection.close()

insert_query_values = (word,t,start_of_current,end_of_current,current_p_occurences,current_total_count)
insert_value(insert_query_values)
print('Successfully insert all information needed for calculating frequency of p at time t!')


# print the record of the word_current_count table -- not necessarily to print this.
cur.execute("SELECT * FROM word_current_count")
records = cur.fetchall()
print(records)
conn.commit()

#close the cursor and connection to PostgreSQL.
cur.close()
conn.close()

