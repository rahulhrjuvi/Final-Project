/* change your database to FINAL_PROJECT using the command "\c FINAL_PROJECT" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
drop table if exists tweets;
CREATE TABLE tweets (
tweet_id VARCHAR (2000) PRIMARY KEY,
time_stamp timestamp NOT NULL,
tweet VARCHAR (2000) NOT NULL);

/* creating a table called word_count to store timestamp of word input, word and frequency */
drop table if exists word_count;
create table word_count (
time_stamp timestamp NOT NULL,
word varchar(50) NOT NULL,
freq numeric);
