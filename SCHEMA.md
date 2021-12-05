**tweets**: *tweet_id, time_stamp,* tweet
> This table is simply storing data from what we get from Twitter API / an existed file
**word_current_count**: *p, start_of_current_time, t*, p\_current\_freq, 
> This table stores the words and phrases, as in column p, appear at the current time. And it also stores t as the time now and the word count in the current minute.
**unique_words_current**: *start_of_current_minute, t*, uniq\_wph\_current_count
> This table stores the start of the current minute and the t as the time right now, and also has the unique words count in that current minute.
**tweets_backup**: *tweet_id, time_stamp,* tweet
> It’s a backup table of tweets. In case that the main table was deleted.

### How?
In this schema, once we have all the tweets in our data warehouse, we have the word count and unique word frequency in current minute, then we can compute the prior minute and then get the trendiness score.

