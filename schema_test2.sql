CREATE database final_project;
/* change your database to final_project using the command "\c final_project" */

/* creating a table called tweets to store tweet_id, timestamp and the tweet */
drop table if exists tweets;
CREATE TABLE tweets (
tweet_id varchar (2000) PRIMARY KEY,
time_stamp timestamp NOT NULL,
tweet varchar (2000) NOT NULL);

/* creating a table called word_current_count to store frequency of p in current minute at t*/
drop table if exists word_current_count;c
create table word_current_ccount (
p VARCHAR(100)  PRIMARY KEY NOT NULL,
t timestamp NOT NULL,
start_of_current_minute timestamp NOT NULL,
end_of_current_minute timestamp NOT NULL,
p_current_freq numeric NOT NULL,
total_p_current numeric NOT NULL,
v_current numeric NOT NULL);

/* creating a table called word_prior_count

