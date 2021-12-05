#importing libraries
import sys
import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg2


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

# open a connection (close it later)
conn = psycopg2.connect(database="final_project", user="gb760")
# create a cursor
cur = conn.cursor()
# execute a SQL command
query = """
select time_stamp from tweets order by 1 desc limit 1;
"""
cur.execute(query)
tm = []
tm = cur.fetchall()
t = tm[0][0]
start_of_current = ceil_dt(t, timedelta(minutes=-1)) 
end_of_current = t

# open a connection (close it later)
conn = psycopg2.connect(database="final_project", user="gb760")
# create a cursor
cur = conn.cursor()
# execute a SQL command
query = """
select * from tweets where time_stamp>='"+str(start_of_current)+"' and time_stamp<='"+str(end_of_current)+"';
"""
cur.execute(query)
tweets = []
tweets = cur.fetchall()
time_lst = [tweets[x][1] for x in range(len(tweets))]
text_lst = [tweets[x][2] for x in range(len(tweets))]


#repeating the same progress in part C
def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta


def current_text_fnc(text, start_of_current, end_of_current):
    current_text = []
    for i in range(len(text)):
        if time_lst[i]>=start_of_current and time_lst[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

#unprocessed tweet text list of current minute at t
current_text = current_text_fnc(text_lst, start_of_current, end_of_current)

#def vocabulary_size()
def vocabulary_size(text):
    #get a list of processed words.
    tweets_string = ' '.join(text) 
    tweets_string = preprocess(tweets_string) #put all processed tweets texts into a single string.
    tweet_words = tweets_string.split(' ') #split the string into a list with space.
    tweet_words = list(filter(lambda a: a != '', tweet_words)) #drop the ''.
    tweet_words = [item for item in tweet_words if item[0] != '#'] #drop the remaining sign '#'.
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


#get the number of unique words in the current minute at t
unique_word_count = vocabulary_size(current_text)

#print the frequency of p in the current minute at t
print("The number of unique words used in the tweets posted in the current minute t = ", str(t), "is", unique_word_count, "!")


# insert values into unique_words_current_count table
def insert_value(insert_query_values):
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()              
    query = """INSERT INTO unique_words_current_count (start_of_current_minute,uniq_wph_current_count)
VALUES (%s,%s)"""           
    cursor.execute(query, insert_query_values)
    connection.commit()           
    if connection:
        cursor.close()
        connection.close()

insert_query_values = (end_of_current,unique_word_count)
insert_value(insert_query_values)
print('Insertion into table done!')


# print the record of the unique_words_current_count table -- not necessarily to print this.
cur.execute("SELECT * FROM unique_words_current_count")
records = cur.fetchall()
print(records)
conn.commit()

#close the cursor and connection to PostgreSQL.
cur.close()
conn.close()
