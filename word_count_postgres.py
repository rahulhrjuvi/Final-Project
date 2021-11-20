import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg

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

#https://stackoverflow.com/questions/13071384/ceil-a-datetime-to-next-quarter-of-an-hour
def ceil_dt(dt, delta):
    return datetime.min + math.ceil((dt - datetime.min) / delta) * delta

def prior_text(text, start_of_prior, end_of_prior):
    prior_text = []
    for i in range(len(text)):
        if time[i]>=start_of_prior and time[i]<=end_of_prior:
            prior_text.append(text[i])
    return prior_text

def current_text(text, start_of_current, end_of_current):
    current_text = []
    for i in range(len(text)):
        if time[i]>=start_of_current and time[i]<=end_of_current:
            current_text.append(text[i])
    return current_text

def calculation_numbers(text, my_input):
    tweets_string = ' '.join(text)
    tweets_string = preprocess(tweets_string)
    tweet_words = tweets_string.split(' ')
    tweet_words = list(filter(lambda a: a != '', tweet_words))
    tweet_words = [item for item in tweet_words if item[0] != '#']# see the issue

    if ' ' in my_input:
        my_input = my_input.split(' ')
        phrase_list = []
        for i in range(len(tweet_words)-1):
            phrase_list.append(tweet_words[i:i+2])
        phrase_list_set = set(tuple(x) for x in phrase_list)
        count = phrase_list.count(my_input)
        return count, len(phrase_list), len(phrase_list_set)
    else:
        tweet_words_set = set(tweet_words)
        count = 0
        count += tweets_string.count(my_input)
        return count, len(tweet_words), len(tweet_words_set)

# open a connection (make sure to close it later)
conn = psycopg.connect("dbname=final_project user=gb760")
# create a cursor
cur = conn.cursor()
#cur.execute(open("schema_test.sql", "r").read())
#conn.commit()
# execute a SQL command
query = """
select * from tweets;
"""
cur.execute(query)
cur.close()
conn.close()

tweets = []
for row in cur:
    tweets.append(row)
time = [tweets[x][1] for x in range(len(tweets))]
text = [tweets[x][2] for x in range(len(tweets))]

start_of_prior = ceil_dt(time[0], timedelta(minutes=1))
end_of_prior = start_of_prior + timedelta(seconds = 59)
start_of_current = time[0]+timedelta(minutes = 2)
end_of_current = ceil_dt(start_of_current, timedelta(minutes=1)) - timedelta(seconds = 1)

my_input = 'machine learning'

##### PRIOR MINUTE
prior_text = prior_text(text, start_of_prior, end_of_prior)
prior_occurences, prior_total_count, prior_unique_count = calculation_numbers(prior_text,my_input)

##### CURRENT MINUTE
current_text = current_text(text, start_of_current, end_of_current)
current_occurences, current_total_count, current_unique_count = calculation_numbers(current_text,my_input)

##### FINAL CALCULATION

prob_prior = (1+prior_occurences)/(prior_total_count+prior_unique_count)
prob_current = (1+current_occurences)/(current_total_count+current_unique_count)
trendiness_score = np.log(prob_current/prob_prior)
trendiness_score