import re
import math
from datetime import timedelta
import numpy as np
import psycopg
import time
import argparse
import datetime
import pause, datetime



# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--word', type=str, required=True)
# Parse the argument
args = parser.parse_args()
word = args.word

#getting the time at which trendiness score code is run
entry_time = datetime.datetime.now().replace(microsecond=0) + timedelta(hours = 6)
code_start = datetime.datetime.now().replace(microsecond=0)
start_time = code_start+timedelta(seconds = 58 - code_start.second)

#pausing until the end of the minute at which trendiness score code is run
pause.until(start_time)

#processing the tweets
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
    tweet_words = [item for item in tweet_words if item[0] != '#']

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

# open a connection (make sure to close it later)
conn = psycopg.connect("dbname=final_project user=gb760")
# create a cursor
cur = conn.cursor()

#compute initial start and end of current and prior minute
start_of_prior = entry_time-timedelta(seconds = entry_time.second)-timedelta(minutes=1)
end_of_prior = entry_time+timedelta(seconds = 59 - entry_time.second)-timedelta(minutes=1)
start_of_current = entry_time-timedelta(seconds = entry_time.second)
end_of_current = entry_time+timedelta(seconds = 59 - entry_time.second)


while True:
    # execute a SQL command to filter only 2 minutes of data
    query = "select * from tweets_kafka where time_stamp>='"+str(start_of_prior)+"' and time_stamp<='"+str(end_of_current)+"';"
    cur.execute(query)
    

    tweets = []
    for row in cur:
        tweets.append(row)
    time = [tweets[x][0] for x in range(len(tweets))]
    text = [tweets[x][1] for x in range(len(tweets))]

    ##### PRIOR MINUTE
    prior_text = prior_text_fnc(text, start_of_prior, end_of_prior)
    prior_occurences, prior_total_count, prior_unique_count = calculation_numbers(prior_text,word)

    ##### CURRENT MINUTE
    current_text = current_text_fnc(text, start_of_current, end_of_current)
    current_occurences, current_total_count, current_unique_count = calculation_numbers(current_text,word)

    ##### FINAL CALCULATION

    prob_prior = (1+prior_occurences)/(prior_total_count+prior_unique_count)
    prob_current = (1+current_occurences)/(current_total_count+current_unique_count)
    trendiness_score = np.log(prob_current/prob_prior)
    print("Trendiness score for the word/phrase", word, "is", trendiness_score, "at time", start_of_current)
    
    with open('trendiness_score.csv','a') as fd:
        fd.write('\n')
        fd.write(str(start_of_current)[11:16]+', '+str(trendiness_score))
    
    #compute new start and end time
    start_of_prior+= timedelta(minutes = 1)
    end_of_prior+= timedelta(minutes = 1)
    start_of_current+= timedelta(minutes = 1)
    end_of_current+= timedelta(minutes = 1)
    start_time+= timedelta(minutes = 1)
    
    pause.until(start_time)
    
 
    
