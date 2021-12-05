CREATE database final_project;
/* change your database to final_project using the command "\c final_project" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
drop table if exists tweets;
CREATE TABLE tweets (
tweet_id varchar (2000),
time_stamp timestamp NOT NULL,
tweet varchar (2000) NOT NULL,
PRIMARY KEY (time_stamp, tweet_id))
PARTITION BY RANGE (time_stamp);

CREATE INDEX idx_tm 
ON tweets(time_stamp);

CREATE TABLE p0 PARTITION OF tweets FOR VALUES FROM (current_date) TO (current_date + interval '1 day');

/* creating a table called tweets_backup to store tweet_id, timestamp and the tweet in case main table gets deleted */
drop table if exists tweets_backup;
CREATE TABLE tweets_backup (
tweet_id varchar (2000),
time_stamp timestamp NOT NULL,
tweet varchar (2000) NOT NULL,
PRIMARY KEY (time_stamp, tweet_id))
PARTITION BY RANGE (time_stamp);

CREATE INDEX idx_tm_bkp 
ON tweets_backup(time_stamp);

CREATE TABLE p0_backup PARTITION OF tweets_backup FOR VALUES FROM (current_date) TO (current_date + interval '1 day');

/* creating a table called word_current_count to store frequency of p in current minute at t*/
drop table if exists word_current_count;
create table word_current_count (
p VARCHAR(100)  PRIMARY KEY NOT NULL,
t timestamp NOT NULL,
start_of_current_minute timestamp NOT NULL,
end_of_current_minute timestamp NOT NULL,
p_current_freq numeric NOT NULL,
total_p_current numeric NOT NULL);

/* creating a table called unique_word_count to store the number of unique words used in the tweets posted in the current minute t*/
drop table if exists uniq_word_count;
create table uniq_word_count (
t timestamp NOT NULL,
start_of_current_minute timestamp NOT NULL,
end_of_current_minute timestamp NOT NULL,
uniq_word_count numeric NOT NULL);

/* creating a table called word_prior_count

