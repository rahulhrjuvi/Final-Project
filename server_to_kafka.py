# To detect the language in text
# Reference: https://stackoverflow.com/questions/39142778/python-how-to-determine-the-language
import langid
import config
import argparse
import sys
import json 
from kafka import KafkaProducer
from json import dumps
import requests
import os
import json

bearer_token = config.BEARER_TOKEN

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at"

# Same as "def bearer_oauth" in the sample string code
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r
    
def parse_timestamp(s):
    # Delete the unnecessary part of the date and time, change the colons to the hyphens
    date = s.split('T')[0]
    time = s.split('T')[1].split('.000Z')[0].replace(":", "-")
    timestamp = date + "-" + time
    return timestamp

def parse_json(json_response): 
    if langid.classify(json_response["text"])[0] == 'en':
        # Store time and text into two variables
        # We only want text in English, and thus we need a filter
        res_time = parse_timestamp(json_response["created_at"])
        res_text = json_response["text"].splitlines()
        res_text = ''.join(str(e) for e in res_text)
        res = res_time + ", " + res_text
        return res
    
    
if __name__ == "__main__":
    url = create_url()
    
    #Parsing 
    parser = argparse.ArgumentParser(description='File/API.')
    parser.add_argument("--file", help="Generates a file of tweets.", default="")
    args = parser.parse_args()
    file = args.file
    if file == '': #### TWIITER API ####
        print ("Pushing tweets into stream using Twitter API")
        
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:  
                         dumps(x).encode('utf-8'))
        
     
        # The original code in "def connect_to_endpoints" in sample string code
        while True:
            response = requests.request("GET", url, auth = bearer_oauth, stream = True)
            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                    response.status_code, response.text))
            for response_line in response.iter_lines():
                if response_line:
                    #if (os.path.getsize('tweets.txt')>2000000):
                        #sys.exit()
                    json_response = json.loads(response_line)["data"]
                    
                    dat = parse_json(json_response)
                    producer.send('gb760', value=dat)
                          
            timeout += 1
    else: #### JSON TWEETS ####
        print ("Pushing tweets into stream using JSON Tweets")
        time = 0
        json_datas = json.load(json_file)["data"]
        for json_response in json_datas:
            dat = parse_json(json_response)
            producer.send('gb760', value=dat)
