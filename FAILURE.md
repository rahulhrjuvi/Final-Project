# List of Failures

## Incorporated in Code:

1. tweets.txt might get corrupted or lost due to some system error. **Generating a backup file simultaneously**.

2.  Stopping once the tweets.txt reaches a size of 5 MB as above that, the rate limit might be reached.

3.  Exception handling in cases where credentials are wrong or the internet is not working.


## Not Incorporated in Code:

1.  Rate Limit for Twitter API.

2.  High CPU Usage during fetching of Tweets and inserting in tweets.txt.

3.  High RAM Usage during fetching of Tweets and inserting in tweets.txt.
