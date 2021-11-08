import requests
import os
import json
import langid
import argparse

def parse_timestamp(s):
    date = s.split('T')[0]
    time = s.split('T')[1].split('.000Z')[0].replace(":", "-")
    timestamp = date + "-" + time
    return timestamp

with open('test') as json_file:
    f= open("tweets2.txt","w+")
    time = 0
    json_datas = json.load(json_file)["data"]
    for json_response in json_datas:
        if langid.classify(json_response["text"])[0] == 'en':
            res_time = parse_timestamp(json_response["created_at"])
            res_text = json_response["text"].splitlines()
            res_text = ''.join(str(e) for e in res_text)
            res = res_time + ", " + res_text + "\n"
            f.write(res)   
    f.close()