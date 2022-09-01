# **Twitter Trendiness Score Project**

The objective of this project is to compute the trendiness scores of specific words and phrases (two consecutive words) appearing in Twitter.

What is a "Trend"?   
Spikes in the likelihood of seeing a word/phrase relative to its usual likelihood.

<img width="300" alt="Trend" src="https://user-images.githubusercontent.com/89796629/147373404-6ea2b21a-bc21-4581-9838-f25f3488b0dd.png">

**“Trendiness Score” Formula:**        
The trendiness of a word/phrase p at time t is computed as follows.:

<img width="490" alt="Formula1" src="https://user-images.githubusercontent.com/89796629/147373766-06b736c0-f82e-449d-a7ce-8efd68cda181.png">

Here, V is the count of unique words/phrases and,

<img width="753" alt="Formula2" src="https://user-images.githubusercontent.com/89796629/147373771-c60dd90e-6be9-4964-a653-fb1e78b181b0.png">

### Approach

Tweets are obtained from the Twitter API.  

Each individual tweet along with its timestamp is transformed according to our needs and pushed to a Kakfa Queue.  

At the consumer end, the tweets are consumed and loaded onto a Tweets table in a PostgreSQL Database.  

Now, when a user wants to find out the trendiness score of a word/phrase at any specific time, the user runs the trendiness_kafka.py script with the word/phrase as input.   

The trendiness score of the word/phrase is computed using the formula shown above and displayed.  

This process is executed every minute until the code is force stopped.    

Finally, trendiness scores are plotted across each minute.    

The same is shown below:

<img width="450" alt="Trendiness" src="https://user-images.githubusercontent.com/89796629/147373692-b2ebee08-0eec-4734-ad1a-a71d0145ad8e.png">

