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
select * from tweets;
"""
cur.execute(query)

#get the tweets content list - each row of the table tweets is a tuple
tweets_lst = cur.fetchall()
time_lst = [tweets_rows[1] for tweets_rows in tweets_lst]
text_lst = [tweets_rows[2] for tweets_rows in tweets_lst]

#repeating the same progress in part C
def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

t = time_lst[0]+timedelta(minutes = 2)
start_of_current = ceil_dt(t, timedelta(minutes=-1)) 
end_of_current = ceil_dt(t, timedelta(minutes=1)) - timedelta(seconds = 1)


def current_text(text, start_of_current, end_of_current):
    current_text = []
    for i in range(len(text)):
        if time_lst[i]>=start_of_current and time_lst[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

#unprocessed tweet text list of current minute at t
current_text = current_text(text_lst, start_of_current, end_of_current)

#def vocabulary_size()
def vocabulary_size(text):
    #get a list of processed words.
    tweets_string = ' '.join(text) 
    tweets_string = preprocess(tweets_string) #put all processed tweets texts into a single string.
    tweet_words = tweets_string.split(' ') #split the string into a list with space.
    tweet_words = list(filter(lambda a: a != '', tweet_words)) #drop the ''.
    tweet_words = [item for item in tweet_words if item[0] != '#'] #drop the remaining sign '#'.
    uniq_words = set(tweet_words)
    uniq_count = len(uniq_words)
    return uniq_count

#get the number of unique words in the current minute at t
unique_word_count = vocabulary_size(current_text)

#print the frequency of p in the current minute at t
print("The number of unique words used in the tweets posted in the current minute t = ", str(t), "is", unique_word_count, "!")

# reset uniq_word_count table
def reset_uniq_word_count_table():
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE uniq_word_count""")
    connection.commit()
    if connection:
        cursor.close()
        connection.close()

reset_uniq_word_count_table()  


# insert values into uniq_word_count table
def insert_value(insert_query_values):
    connection = psycopg2.connect(user="gb760", dbname = "final_project")
    cursor = connection.cursor()              
    query = """INSERT INTO uniq_word_count (t,start_of_current_minute,end_of_current_minute,uniq_word_count)
VALUES (%s,%s,%s,%s)"""           
    cursor.execute(query, insert_query_values)
    connection.commit()           
    if connection:
        cursor.close()
        connection.close()

insert_query_values = (t,start_of_current,end_of_current,unique_word_count)
insert_value(insert_query_values)
print('Successfully insert all information needed for calculating the number of unique words at time t!')


# print the record of the uniq_word_count table -- not necessarily to print this.
cur.execute("SELECT * FROM uniq_word_count")
records = cur.fetchall()
print(records)
conn.commit()

#close the cursor and connection to PostgreSQL.
cur.close()
conn.close()
