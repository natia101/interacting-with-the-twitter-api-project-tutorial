import os
import pandas as pd
import numpy as np
import tweepy
import requests
import re
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv


# Load the .env file variables
load_dotenv()

# App code here
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
bearer_token = os.environ.get('BEARER_TOKEN')

# Client
client = tweepy.Client( bearer_token=bearer_token,
consumer_key=consumer_key,
consumer_secret=consumer_secret,
return_type = requests.Response,
wait_on_rate_limit=True)

# Twitter query
query = '#100daysofcode (pandas OR python) -is:retweet'

# Twitts related to query
tweets = client.search_recent_tweets(query=query,
tweet_fields=['author_id','created_at','lang'],
max_results=100)

# Save as dictionary
tweets_dict = tweets.json()
tweets_dict.keys()

# Extract data
tweets_data = tweets_dict['data']

# Transform to pandas DF
df = pd.json_normalize(tweets_data)

df.head()

# Save as .csv
df.to_csv('coding-tweets.csv')

# Search for the words 'python' and 'pandas'

# Function that returns "yes" if it finds the word and "no" otherwise.
def word_in_text(word,tweet):
    t=tweet
    t=t.lower()
    w=re.compile(word)
    if w.search(t) is not None :
        return('Yes')
    else :
            return('No')


#testing the function
word_in_text('python','the best lenguage is Python')


n_py=0
n_pd=0

for lab,row in df.iterrows():
    if word_in_text('python',row['text']) == 'Yes' :
        n_py+=1
    if word_in_text('pandas',row['text']) == 'Yes' :
        n_pd+=1
    
print (f'Python {n_py} // Pandas {n_pd}')

# Plot quantity of words

sns.set_theme(style="ticks", color_codes=True)

cd=['Python','Pandas']

ax = sns.barplot(cd,[n_py,n_pd])
ax.set(ylabel='Count',title='Python and pandas tweets')
plt.show()
