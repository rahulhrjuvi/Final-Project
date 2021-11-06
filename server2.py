# Structure: Twitter API sample string code
import requests
import os
import json
# To detect the language in text
# Reference: https://stackoverflow.com/questions/39142778/python-how-to-determine-the-language
import langid
import argparse
# Open the input test file, provide the filename in bracket
with open('test.json') as json_file:
        
    def parse_timestamp(s):
    # Delete the unnecessary part of the date and time, change the colons to the bars
        date = s.split('T')[0]
        time = s.split('T')[1].split('.000Z')[0].replace(":", "-")
        timestamp = date + "-" + time
        return timestamp

    
    # Create and open the tweets.txt
    f= open("tweets2.txt","w+")
    time = 0
    
    # The original code in "def connect_to_endpoints" in sample string code
    while True:
        json_datas = json.load(json_file)["data"]
        for json_response in json_datas:
            # Call the data we really need
            # Reference: https://www.kite.com/python/answers/how-to-extract-a-value-from-json-in-python
            # Store time and text into two variables
            # We only want text in English, and thus we need a filter
            if langid.classify(json_response["text"])[0] == 'en':
                res_time = parse_timestamp(json_response["created_at"])
                res_text = json_response["text"].splitlines()
                res_text = ''.join(str(e) for e in res_text)
                # Combine the time and text, make them into one line
                res = res_time + ", " + res_text + "\n"
                f.write(res)
                # To see what's in the file, we set a print function
                print(res)
                 
        f.close()

