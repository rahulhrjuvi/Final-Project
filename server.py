# Structure: Twitter API sample string code
import requests
import os
import json

bearer_token = os.environ.get("BEARER_TOKEN")

# Call the url
# Since we need the time, give endpoint as ?tweet.fields=created_at, based on Twitter API documentation

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

if __name__ == "__main__":
    url = create_url()
    
    # Create and open the tweets.txt
    f= open("tweets.txt","w+")
    time = 0
    
    # The original code in "def connect_to_endpoints" in sample string code
    while True:
        response = requests.request("GET", url, auth = bearer_oauth, stream = True)
        print(response.status_code)
        for response_line in response.iter_lines():
            if response_line:
                # Call the data we really need
                json_response = json.loads(response_line)["data"]
                # Store time and text into two variables
                res_time = json_response["created_at"]
                res_text = json_response["text"]
                # Combine the time and text, make them into one line
                res = res_time + "  ,  " + res_text
                f.write(res)
                f.write("\n")
                # To see what's in the file, we set a print function
                print(res)
            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                    response.status_code, response.text)
                )
        f.close()
        timeout += 1
