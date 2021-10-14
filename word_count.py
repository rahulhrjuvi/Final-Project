#Importing libraries
import argparse
import re


#Parsing functionality
parser = argparse.ArgumentParser(description='Computes Word/Phrase Frequency.')
parser.add_argument("--word", help="Computes Word/Phrase Frequency.", default='GB760')
args = parser.parse_args()
word = args.word
print ("Computing Frequency for '",word,"'!" )


#Getting all text from tweets.txt and converting to a string called 'data'
text_file = open("tweets.txt", "r")
data = text_file.read()
text_file.close()
data = data.replace('\n','')


#splitting it on date comma and then space as this is how our tweets.txt was generated (using regular expression)
data = re.split('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9], ',data)
data = data[1::]


#Computing final count for word/phrase using Python's in built count function
myword = word
count = 0
for i in data:
    count += i.count(myword)


#Printing out
print ("The word/phrase count for '",word,"' is ",count,'!')
