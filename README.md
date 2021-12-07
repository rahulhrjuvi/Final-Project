# GENBUS760 - Final Project 

> Group 8

> NANCY TAI, COLIN KONG, RUIYU MIN, MOIZ SADIQ AWAN, RAHUL HUNASEHALLI RUDRANNA GOWDA, SIJIA GE

## Beforehand Set Up
Please make sure you need all packages needed in the codes. If not, please install them first.
Important packages include:
> json, langid, argparse, sys, numpy, re, psycopg, psycopg2, pause

## Milestone I
**Please run the code in this order: server.py > word_count.py > vocabulary_size.py**
### Part A
Run the server.py file in the terminal in python3.

If you would like to read tweets from an existing file, you have to type in "--file 'xxx'", input the file you would like to parse json tweets from in the quotation marks.  
For example, you can try: 
```
python server.py --file 'tweets.json'
```
If you do not type in anything, it will get tweets from Twitter API. If you would like to stop reading, press **Ctrl+C**.
If you would like to read tweets from Twitter API, you can try:  
```
python server.py
```

### Part B
Put the document "tweets.txt", which is generated from Part A, and "word_count.py" under the same folder.  
For example, if you're folder's name is "Final_Project", then you can try to call: 
```
cd ~
cd Final-Project
```

Then, run the word_count.py file in the terminal in python3 after changing directory to that folder.  
You have to type in "--word 'xxx'", input the word or phrases you would like to search in the quotation marks to get the result of count.

If you do not type in anything, it will jump out a sentence to remind you of that!  
Here are some examples of commands you can try:
```
python word_count.py
python word_count.py --word 'we'
python word_count.py --word 'we are'
```

### Part C
Put the document "tweets.txt" and "vocabulary_size.py" under the same folder, and run the vocabulary\_size\_.py file in the terminal in python3 after changing directory to that folder.   
After running the .py file, it will print the number of unique words used in all the tweets stored in tweets.txt.  
Example you can try:
```
python vocabulary_size.py
```

### Part D
Please refer to FAILURE.md.

### Part E
Please check the tag name: **Milestone1**

## Milestone II
**Please run the code _in this order_ after input the schema: server_postgres.py > word_count_postgres.py > vocabulary_size_postgres.py > trendiness_score.py**

### Part A
Please refer to SCHEMA.md to see how we designed our schema.  
To import the schema, please create the database using psql. 
```
psql
create database final_project;
\q
```
Then, let's import the tables. Call in your terminal: 
```
psql final_project < schema_postgres.sql

```

### Part B
Run the server_postgres.py file in the terminal in python3.

If you would like to read tweets from an existing file, you have to type in "--file 'xxx'", input the file you would like to parse json tweets from in the quotation marks.  
For example, you can try: 
```
python server_postgres.py --file 'tweets.json'
```
If you do not type in anything, it will get tweets from Twitter API!  
If you would like to read tweets from Twitter API, you can try: 
```
python server_postgres.py
```
To stop reading, please press **Ctrl+C**.

### Part C
Keep running the server_postgres.py in the terminal in python3: 
```
python server_postgres.py
```
Then, run the word\_count\_postgres.py file in the terminal in python3. It will print the frequency of p in the current minute at t and store each record of your search into schema table word\_current\_count.  

You have to type in "--word 'xxx'", input the word or phrases you would like to search in the quotation marks to get the result of count.  
If you do not type in anything, it will jump out a sentence to remind you of that!  
Here are some examples of commands you can try:
```
python word_count_postgres.py
python word_count_postgres.py --word 'we'
python word_count_postgres.py --word 'We'
python word_count_postgres.py --word 'we are'
```

You can search for the same word/phrase more than once to store the record of different time in the word\_current\_count table for further analysis.  
For example, to see the word\_current\_count table:
```
psql
select * from word_current_count;
\q
```
An example of word_current_count table:  
|p       | start\_of\_current\_minute |          t          | p\_current_freq|  
|:-------|:-----------------------:|:-------------------:|--------------:|
| we     | 2021-12-05 18:07:00     | 2021-12-05 18:07:18 |             21|
| we     | 2021-12-05 18:07:00     | 2021-12-05 18:07:38 |             81|
| we     | 2021-12-05 18:07:00     | 2021-12-05 18:07:49 |            115|
| we are | 2021-12-05 18:09:00     | 2021-12-05 18:09:37 |              1|
| we are | 2021-12-05 18:09:00     | 2021-12-05 18:09:57 |              2|
| we are | 2021-12-05 18:10:00     | 2021-12-05 18:10:01 |              0|


### Part D
Keep running the server_postgres.py in the terminal in python3.  
Then run the vocabulary\_size\_postgres.py file in the terminal in python3. It will print the number of unique words used in the tweets posted in the current minute at t and store the record into schema table unique\_words\_current_count every time you run the command:
```
python vocabulary_size_postgres.py
```
For example, to see the unique\_words\_current_count table:
```
psql
select * from unique_words_current_count;
\q
```
An example of unique_words_current_count table:  
| start_of_current_minute|          t          | uniq_wph_current_count|
|:----------------------:|:-------------------:|----------------------:|
| 2021-12-05 18:10:00    | 2021-12-05 18:10:34 |                   7578|
| 2021-12-05 18:10:00    | 2021-12-05 18:10:39 |                   8191|
| 2021-12-05 18:10:00    | 2021-12-05 18:10:51 |                  10281|
| 2021-12-05 18:11:00    | 2021-12-05 18:11:01 |                    485|
| 2021-12-05 18:11:00    | 2021-12-05 18:11:19 |                   4330|
| 2021-12-05 18:11:00    | 2021-12-05 18:11:40 |                   8775|

### Part E
Keep running the server_postgres.py in the terminal in python3.  
Then run the trendiness\_score.py file in the terminal in python3. It will print the trendiness score of the word/phrase you input in the current minute t.

You have to type in "--word 'xxx'", input the word or phrases you would like to compute the trendiness score for in the quotation marks to get the result of score. 
If you do not type in anything, it will jump out a sentence to remind you of that!  
Here are some examples of commands you can try:
```
python trendiness_score.py --word 'omicron'
python trendiness_score.py --word 'machine learning'
python trendiness_score.py --word 'data engineering'
```
The output will be in the following form:
```
Trendiness score for the minute 2021-12-06 12:30:00 is 2.37
```

## Milestone III
**Please run the code _in this order_ after input the schema: kafka_zookeeper_kafka_start.md > server_to_kafka.py > server_from_kafka.py > trendiness_kafka.py**


### Part A
First, run the commands in kafka_zookeeper_kafka_start.md in order to start zookeeper and kafka servers.
Get into the folder where the kafka scripts are saved and start server_to_kafka.py code. This will start getting the tweets from the API/JSON file and pushing them into kafka.

### Part B
Now, after Part A is done, run the script server_from_kafka.py in a different command window. This will start consuming the tweets from kafka and push them into the TWEETS table in psql.

NOTE: Both these scripts are going to run non-stop until they are stopped forcefully.
NOTE: We have to let these codes run for atleast 1 minute so that we have prior minute data.

### Part C
Now, once we have atleast 1 minute data in our table TWEETS, we can run the trendiness_kafka.py script, in a different command window, in order to compute the trendiness score for the word entered by the user. The trendiness score is calculated for every minute after this code is run.

You have to type the following in the command window: **python trendiness_kafka.py --word "<your word/phrase>"**

Let me provide an example to understand it better:

Lets assume we run server_to_kafka.py at time 12:00:00.
Now, lets run server_from_kafka.py at the same time, 12:00:00.
Now, we wait for, lets say 1.5 minutes so that we have prior minute data in our database.

Now, lets say the time is 12:01:30.

Now, we execute trendiness_kafka.py. This code is going to wait until the end of the current minute which is, 12:01:59.
As soon as we hit this time mark, the code is going to run and print the trendiness score at this time mark.

Now, the code is going to pause for 1 minute in order to generate the next minute data.

Now, lets assume the code paused for 1 minute. Now the start of prior, end of prior, start of current and end of current timestamps are as follows:

start of prior: 12:01:00
end of prior: 12:01:59
start of current: 12:02:00
end of current: 12:02:59

Now, the trendiness score is calculated for the above time filters and printed. This process is going to run until eternity, unless stopped forcefully.

### Additional Feature
When trendiness_kafka.py is started, you should run trendiness_score_plot.py in a terminal window. It will open up a Matplotlib window for real-time trend plot of the trendiness score. 
