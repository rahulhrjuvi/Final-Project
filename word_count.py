#Importing libraries
import argparse
import re
import sys

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

#Parsing functionality
parser = argparse.ArgumentParser(description='Computes Word/Phrase Frequency.')
parser.add_argument("--word", help="Computes Word/Phrase Frequency.", default="")
args = parser.parse_args()
word = args.word
if word == '':
    print ("You need to use <python3 word_count.py --word 'xxx'> and put the word or phrases you want to compute frequency in the argument 'xxx'!")
    sys.exit()
print ("Computing Frequency for '",word,"'!" )
word = ' '+word+' ' 

#Getting all text from tweets.txt and converting to a string called 'data'
text_file = open("tweets.txt", "r")
data = text_file.read()
text_file.close()
data = data.replace('\n','')

#splitting it on date comma and then space as this is how our tweets.txt was generated (using regular expression)
data = re.split('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9], ',data)
data = data[1::]

#adding in spaces before and after to avoid 'this is' vs 'is', tweets preprocessing
for i in range(len(data)):
    data[i] = ' '+data[i]+' '
    data[i] = preprocess(data[i])

#Computing final count for word/phrase using Python's in built count function
myword = word
count = 0
for i in data:
    count += i.count(myword)

#Printing out
print ("The word/phrase count for '",word,"' is ",count,'!')
