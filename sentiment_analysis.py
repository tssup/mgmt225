from lib2to3.pytree import convert
import pandas as pd
import requests
import os
import json
import sys
import time
import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

hashtag = str(sys.argv[1])

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': hashtag, 'user.fields': 'username'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
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


x_vals = []
y_vals = []
z_vals = []


def main(i):

    current_time = datetime.datetime.now()

    tweets = convert_to_dataframe()
    tweets['sentiment score'] = tweets['Tweet'].apply(get_polarity)
    average = round(tweets['sentiment score'].mean(), 2)

    plt.cla()
    #plt.ylim([0, 1.0])
    x_vals.append(current_time)
    if average >= 0:
        y_vals.append(average)
        z_vals.append(0)
    else:
        z_vals.append(-average)
        y_vals.append(0)

    plt.fill_between(x_vals, y_vals, color="skyblue",
                     alpha=0.8, label="+ve sentiments")
    plt.fill_between(x_vals, z_vals, color="red",
                     alpha=0.8, label="-ve sentiments")
    """
    plt.stackplot(x_vals, y_vals, z_vals, labels=[
                  "+ve sentiments", "-ve sentiments"], alpha=0.8)

    plt.plot(x_vals, y_vals, color="gray", alpha=0.6, linewidth=2)

    """

    plt.xlabel('Time Elapsed')
    plt.ylabel('Sentiment Scores')
    plt.title(f'Sentiment Trend Chart {sys.argv[1]}')
    plt.legend()

    # time.sleep(0.1)


if __name__ == '__main__':
    plt.style.use("fivethirtyeight")
    ani = FuncAnimation(plt.gcf(), main, interval=4000)
    plt.tight_layout()
    plt.show()
