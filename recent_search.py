from lib2to3.pytree import convert
import pandas as pd
import requests
import os
import json
import sys
import time
from textblob import TextBlob
import warnings
warnings.filterwarnings("ignore")


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

hashtag = str(sys.argv[1])

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': hashtag,'user.fields': 'username'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def convert_to_dataframe():
    json_response = connect_to_endpoint(search_url, query_params)
    data = pd.json_normalize(json_response['data'])
    data.columns = ['Account ID', 'Tweet']
    return data

def get_polarity(tweet):
    return TextBlob(tweet).sentiment.polarity



def main():

    print("Time         Average Sentiment")
    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        df = pd.DataFrame(columns=['Time', 'Average'])


        tweets = convert_to_dataframe()
        tweets['sentiment score'] = tweets['Tweet'].apply(get_polarity)
        #print(tweets)

        average = round(tweets['sentiment score'].mean(), 2)
        df = df.append({'Time' : current_time, 'Average' : average}, ignore_index = True)
        print(f"{current_time}           {average}")
        time.sleep(5)
    


if __name__ == "__main__":
    main()