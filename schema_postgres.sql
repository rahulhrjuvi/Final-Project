CREATE DATABASE FINAL_PROJECT;

/* change your database to FINAL_PROJECT using the command "\c FINAL_PROJECT" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
CREATE TABLE tweets (
tweet_id numeric PRIMARY KEY,
timestamp VARCHAR (50) NOT NULL,
tweet VARCHAR (2000) NOT NULL);

/* creating a table called word_count to store timestamp of word input, word and frequency */
create table word_count (
time_stamp VARCHAR (50) NOT NULL,
word varchar(50) NOT NULL,
freq numeric);
