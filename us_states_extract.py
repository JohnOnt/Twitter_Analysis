import numpy as np
import pandas as pd
import os
import glob
import sys
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")


"""
    NOTES

    - This script takes three arguments year (ex. 2020), month (ex. 3), keyterm in all caps (ex. ALCOHOL)
"""

#--------------------------------------------------------------------
# Rule-Based Matching Lists for SpaCy
#--------------------------------------------------------------------

state_abbv = np.array(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

state_names = np.array(["Alabama", "Alaska", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",  
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",  
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"])

matcher = Matcher(nlp.vocab)

pattern = [{'IS_ALPHA': True}, 
           {'IS_PUNCT': True}, 
           {'IS_ALPHA': True}]

matcher.add("State Abbv", [pattern])

#--------------------------------------------------------------------
# Search Functions
#--------------------------------------------------------------------

def state_search(state, text):
    ind = np.char.find(np.char.upper(text), np.char.upper(state))
    ind[ind >= 0] = 1
    ind[ind == -1] = 0
    return np.sum(ind)

def states_search(text):
    lst = np.array([state_abbv[state_names == state][0] if state_search(state, text) > 0 else '' for state in state_names])
    lst = lst[lst != '']
    if len(lst) > 0:
        return lst[0]
    
    else:
        doc = nlp(str(text))
        matches = matcher(doc)

        if len(matches) > 0:
            match = doc[matches[0][2] - 1]

            if str(match) in state_abbv:
                return str(match)

        # Insert Spacy matcher code here
        return ''


def tweet_search(tweets, df):
    matches = np.vectorize(states_search)(tweets)

    df['state'] = matches
    df = df.loc[matches != '']
    df = df.drop(['urls', 'profile_location', 'geotag_location', 'geotag_country'], axis=1)
    return df

#--------------------------------------------------------------------
# Export Function to return Geolocated Tweet DF
#--------------------------------------------------------------------

def Geolocate_Tweets(df):
    tweet_loc = df['profile_location'].values
    tweet_loc = tweet_loc.astype('<U40')

    geolocated_tweets = tweet_search(tweet_loc, df)

    print("In Rows: ", df.shape[0])
    print("Out Rows: ", geolocated_tweets.shape[0])

    return geolocated_tweets


if __name__ == "__main__":
    keyterm = str(sys.argv[1])


    data_dir = '/media/johnattan/LaCie/Twitter_Terms/' + keyterm + '/' 
    all_files = glob.glob(data_dir + "2*.csv")

    # Keep track of how many tweets there are total and the number containing the key term
    tweet_count = 0
    tweet_count_kw = 0

    li = []

    for filename in all_files:
        print('On file: ', filename)

        df = pd.read_csv(filename, index_col=None, header=0)

        tweet_count += df.shape[0]

        #--------------------------------------------------------------------
        # Parse Tweets for Key Term
        #--------------------------------------------------------------------

        # Vectorize tweet column and set it to numpy string to optimize speed
        tweet_text = df['text'].values
        tweet_text = tweet_text.astype('<U140')

        df_kw = Geolocate_Tweets(df)

        tweet_count_kw += df_kw.shape[0]

        li.append(df_kw)
    

    geo_tweets = pd.concat(li, axis=0, ignore_index=True)


    print('Total kw tweets: ', tweet_count)
    print('Total kw tweets geo: ', tweet_count_kw)

    #--------------------------------------------------------------------
    # Write Geolocated Tweets 
    #--------------------------------------------------------------------

    write_dir = '/media/johnattan/LaCie/Twitter_Terms/' + keyterm + '/' 

    geo_tweets.to_csv(write_dir + 'GEO-Tweets.csv')