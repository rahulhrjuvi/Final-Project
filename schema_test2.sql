CREATE database final_project;
/* change your database to final_project using the command "\c final_project" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
drop table if exists tweets;
CREATE TABLE tweets (
tweet_id varchar (2000) PRIMARY KEY,
time_stamp timestamp NOT NULL,
tweet varchar (2000) NOT NULL);

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
drop table if exists unique_word_count;
create table unique_word_count (
t timestamp NOT NULL,
start_of_current_minute timestamp NOT NULL,
end_of_current_minute timestamp NOT NULL,
uniq_word_count numeric NOT NULL);

/* creating a table called word_prior_count

