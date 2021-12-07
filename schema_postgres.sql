CREATE database final_project;
/* change your database to final_project using the command "\c final_project" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
DROP TABLE if exists tweets;
CREATE TABLE tweets (
tweet_id VARCHAR (2000),
time_stamp TIMESTAMP NOT NULL,
tweet VARCHAR (2000) NOT NULL,
PRIMARY KEY (time_stamp, tweet_id))
PARTITION BY RANGE (time_stamp);

CREATE INDEX idx_tm 
ON tweets(time_stamp);

CREATE TABLE p0 PARTITION OF tweets FOR VALUES FROM (current_date + interval '6 hour') TO (current_date + interval '6 hour' + interval '1 day');

/* creating a table called tweets_backup to store tweet_id, timestamp and the tweet in case main table gets deleted */
DROP TABLE if exists tweets_backup;
CREATE TABLE tweets_backup (
tweet_id VARCHAR (2000),
time_stamp TIMESTAMP NOT NULL,
tweet VARCHAR (2000) NOT NULL,
PRIMARY KEY (time_stamp, tweet_id))
PARTITION BY RANGE (time_stamp);

CREATE INDEX idx_tm_bkp 
ON tweets_backup(time_stamp);

CREATE TABLE p0_backup PARTITION OF tweets_backup FOR VALUES FROM (current_date + interval '6 hour') TO (current_date + interval '6 hour' + interval '1 day');

/* creating a table called word_current_count to store frequency of p in current minute at t*/
DROP TABLE if exists word_current_count;
CREATE TABLE word_current_count (
p VARCHAR(100) NOT NULL,
start_of_current_minute TIMESTAMP NOT NULL,
t TIMESTAMP NOT NULL,
p_current_freq NUMERIC NOT NULL,
PRIMARY KEY (p, start_of_current_minute, t));

CREATE INDEX idx_tm_start 
ON word_current_count(start_of_current_minute);

/* creating a table called unique_words_current_count to store the number of unique words used in the tweets posted in the current minute t*/
DROP TABLE if exists unique_words_current_count;
CREATE TABLE unique_words_current_count (
start_of_current_minute TIMESTAMP NOT NULL,
t TIMESTAMP NOT NULL,
uniq_wph_current_count NUMERIC NOT NULL,
PRIMARY KEY (start_of_current_minute, t));

CREATE INDEX idx_cnt
ON unique_words_current_count(uniq_wph_current_count);

/* creating a table called tweets_kafka to store the timestamp and the tweet for tweets stream using kafka*/
DROP TABLE if exists tweets_kafka; 
CREATE TABLE tweets_kafka (time_stamp TIMESTAMP NOT NULL, tweet VARCHAR (2000) NOT NULL);

CREATE INDEX idx_tm_kafka 
ON tweets_kafka(time_stamp);

