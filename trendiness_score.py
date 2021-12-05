import re
import math
from datetime import datetime, timedelta
import numpy as np
import psycopg
import argparse
import sys

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

def prior_text_fnc(text, start_of_prior, end_of_prior):
    prior_text = []
    for i in range(len(text)):
        if time[i]>=start_of_prior and time[i]<=end_of_prior:
            prior_text.append(text[i])
    return prior_text

def current_text_fnc(text, start_of_current, end_of_current):
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

    tweet_words_set = set(tweet_words)

    words = len(tweet_words)
    words_set = len(tweet_words_set)

    phrase_list = []
    for i in range(len(tweet_words)-1):
        phrase_list.append(tweet_words[i:i+2])
    phrase_list_set = set(tuple(x) for x in phrase_list)

    phrases = len(phrase_list)-len(text)+1
    phrases_set = len(phrase_list_set)-len(text)+1

    total_wph = words+phrases
    total_wph_unique = words_set+phrases_set

    if ' ' in my_input:
        my_input = my_input.split(' ')
        count = phrase_list.count(my_input)
        return(count, total_wph, total_wph_unique)
    else:
        count = tweets_string.count(my_input)
        return(count, total_wph, total_wph_unique)
    

#Parsing functionality
parser = argparse.ArgumentParser(description='Computes Trendiness Score.')
parser.add_argument("--word", help="Computes Trendiness Score..", default="")
args = parser.parse_args()
word = args.word
word = word.lower() #transform everything we input to lowercases.
if word == '':
    print ("You need to use <python trendiness_score.py --word 'xxx'> in the terminal in python3 and put the word or phrases you want to compute trendiness score in the argument 'xxx'!")
    sys.exit()
print ("Computing Trendiness Score for '",word,"'!" )


# open a connection (make sure to close it later)
conn = psycopg.connect("dbname=final_project user=gb760")
cur = conn.cursor()
query = "select time_stamp from tweets order by 1 desc limit 1;"
cur.execute(query)
tm = []
for row in cur:
    tm.append(row)
cur.close()
conn.close()


t = tm[0][0]
start_of_current = ceil_dt(t, timedelta(minutes=-1)) 
end_of_current = t
start_of_prior = start_of_current-timedelta(minutes = 1)
end_of_prior = start_of_current-timedelta(seconds = 1)


conn = psycopg.connect("dbname=final_project user=gb760")
cur = conn.cursor()
query = "select * from tweets where time_stamp>='"+str(start_of_prior)+"' and time_stamp<='"+str(end_of_current)+"';"
cur.execute(query)
tweets = []
for row in cur:
    tweets.append(row)
cur.close()
conn.close()

time = [tweets[x][1] for x in range(len(tweets))]
text = [tweets[x][2] for x in range(len(tweets))]

my_input = word

##### PRIOR MINUTE
prior_text = prior_text_fnc(text, start_of_prior, end_of_prior)
prior_occurences, prior_total_count, prior_unique_count = calculation_numbers(prior_text,my_input)

##### CURRENT MINUTE
current_text = current_text_fnc(text, start_of_current, end_of_current)
current_occurences, current_total_count, current_unique_count = calculation_numbers(current_text,my_input)

##### FINAL CALCULATION

prob_prior = (1+prior_occurences)/(prior_total_count+prior_unique_count)
prob_current = (1+current_occurences)/(current_total_count+current_unique_count)
trendiness_score = np.log(prob_current/prob_prior)

### PRINTING TRENDINESS SCORE
print("Trendiness score for the minute", start_of_current, "is: "+str(trendiness_score))
