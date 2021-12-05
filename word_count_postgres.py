# Milestone 2 Part C word_count_postgres.py

###################### import required packages ######################

import argparse
import sys
import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg2

###################### defined functions ######################

# reference link: https://gist.github.com/aniruddha27/8d112b87ff4014b80f606dc68080066d#file-preprocess_tweets-py
def preprocess(tweet):                                           # Cleaning the tweets
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

#https://stackoverflow.com/questions/13071384/ceil-a-datetime-to-next-quarter-of-an-hour
def ceil_dt(dt, delta):                                           #get the start of minute
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

def current_text_fnc(text, start_of_current, end_of_current):     #get unprocessed tweet text list of current minute at t
    current_text = []
    for i in range(len(text)):
        if time_lst[i]>=start_of_current and time_lst[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

def current_p_count(text, my_input):
    #get a list of processed words.
    tweets_string = ' '.join(text) 
    tweets_string = preprocess(tweets_string)                       #put all processed tweets texts into a single string.
    tweet_words = tweets_string.split(' ')                          #split the string into a list with space.
    tweet_words = list(filter(lambda a: a != '', tweet_words))      #drop the ''.
    tweet_words = [item for item in tweet_words if item[0] != '#']  #drop hashtags start with '#'.
    
    phrase_list = []
    for i in range(len(tweet_words)-1):
        phrase_list.append(tweet_words[i:i+2])
    phrases = len(phrase_list)-len(text)+1
    
    if ' ' in my_input:                                             #my_input is 2 word phrases
        my_input = my_input.split(' ')
        count = phrase_list.count(my_input)
        return(count)
    else:                                                           #my_input is single word
        count = tweets_string.count(my_input) 
        return(count)
    
def insert_value(insert_query_values):                              #store each search record in schema table word_current_count
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()              
    query = """INSERT INTO word_current_count (p,start_of_current_minute,t,p_current_freq)
VALUES (%s,%s,%s,%s)"""
    cursor.execute(query, insert_query_values)
    connection.commit()           
    if connection: #close the cursor and connection to PostgreSQL.
        cursor.close()
        connection.close()

###################### argparse ######################
        
#Parsing functionality
parser = argparse.ArgumentParser(description='Computes Word/Phrase Frequency.')
parser.add_argument("--word", help="Computes Word/Phrase Frequency.", default="")
args = parser.parse_args()
word = args.word
word = word.lower() #transform everything we input to lowercases.
if word == '':
    print ("You need to use <python word_count_postgres.py --word 'xxx'> in the terminal in python3 and put the word or phrases you want to compute frequncy in the argument 'xxx'!")
    sys.exit()
print ("Computing Frequency for '",word,"'!" )

###################### main part ######################

conn = psycopg2.connect(database="final_project", user="gb760")        #open a connection (close it later)
cur = conn.cursor()                                                    #create a cursor
query = """select time_stamp from tweets order by 1 desc limit 1;"""   #execute a SQL command
cur.execute(query)
tm = cur.fetchall()                                                    #get the latest time_stamp as a list, e.g. [(datetime(2021,12,5,15,22,53),)]
cur.close()                                                            #close the cursor and connection
conn.close()
#The time t is the time of posting the lastest tweet when we run the code of open a connection select time_stamp from tweets, during running the server_postgres.py
t = tm[0][0]                                                           #e.g.datetime(2021,12,5,15,22,53)
start_of_current = ceil_dt(t, timedelta(minutes=-1))                   #e.g.datetime(2021,12,5,15,22)
end_of_current = t

conn = psycopg2.connect(database="final_project", user="gb760")
cur = conn.cursor()
query = "select * from tweets where time_stamp>='"+str(start_of_current)+"' and time_stamp<='"+str(end_of_current)+"';"
cur.execute(query)
tweets = cur.fetchall()                                                 #a list of [('tweet_id',t,'tweet'),(),...] in the current minute at t
cur.close()
conn.close()
#get a list of current minute time and a list of unprocessed tweet text in current minute at t
time_lst = [tweets[x][1] for x in range(len(tweets))]
text_lst = [tweets[x][2] for x in range(len(tweets))]

#get the no. of times p was seen in the current minute at t
my_input = word
current_text = current_text_fnc(text_lst, start_of_current, end_of_current)
current_occurences = current_p_count(current_text,my_input)
#print the frequency of p in the current minute at t
print("The word/phrase frequency for '", my_input, "' in the current minute", str(start_of_current), "at time t", str(t), "is", current_occurences, "!")

# insert values into word_current_count table
insert_query_values = (my_input,start_of_current,t,current_occurences)
insert_value(insert_query_values)
print('Insertion into table done!')


