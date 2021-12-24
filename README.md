# **Twitter Trendiness Score Project**

The objective of this project is to compute the trendiness scores of specific words and phrases (two consecutive words) appearing in Twitter.

What is a "Trend"?   
Spikes in the likelihood of seeing a word/phrase relative to its usual likelihood.

<img width="300" alt="Trend" src="https://user-images.githubusercontent.com/89796629/147373404-6ea2b21a-bc21-4581-9838-f25f3488b0dd.png">

**“Trendiness Score” Formula:**        
The trendiness of a word/phrase p at time t is computed as follows:

![image](https://user-images.githubusercontent.com/89796629/147373487-36981f5e-b2a1-4109-b346-c952e5c89842.png)

Here, 

![image](https://user-images.githubusercontent.com/89796629/147373508-3b87443d-c7ba-481f-b417-60f2d1813fe8.png)

### Approach

Tweets were obtained from the Twitter API.  
Each individual tweet along with its timestamp was transformed according to our needs and pushed to a Kakfa Queue.  
At the consumer end, the tweets were consumed and loaded onto a Tweets table in a PostgreSQL Database.  
Now, when a user wants to find the trendiness score of a word/phrase at any specific time, the user runs the trendiness_kafka.py script with the word or phrase as input.   
The tredniness score of the word/phrase is computed using the formula shown above and displayed.   
This process is excuted every minute until the code is force stopped.    
Finally, a plot of trendiness scores every minute is plotted across each minute.    
The same is shown below:



