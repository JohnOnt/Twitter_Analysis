import numpy as np
import pandas as pd
import os
import glob
import sys
import ahocorasick

"""
    NOTES

    - This script takes three arguments year (ex. 2020), month (ex. 3), keyterm in all caps (ex. ALCOHOL)
"""

#--------------------------------------------------------------------
# Rule-Based Matching Lists for SpaCy
#--------------------------------------------------------------------

state_labs = np.array(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

state_abbv = [", AL", ", AK", ", AZ", ", AR", ", CA", ", CO", ", CT", ", DC", ", DE", ", FL", ", GA", 
          ", HI", ", ID", ", IL", ", IN", ", IA", ", KS", ", KY", ", LA", ", ME", ", MD", 
          ", MA", ", MI", ", MN", ", MS", ", MO", ", MT", ", NE", ", NV", ", NH", ", NJ", 
          ", NM", ", NY", ", NC", ", ND", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", 
          ", SD", ", TN", ", TX", ", UT", ", VT", ", VA", ", WA", ", WV", ", WI", ", WY"]

state_names = ["Alabama", "Alaska", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",  
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",  
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

state_dict = {state_abbv[i]: state_labs[i] for i in range(len(state_labs))}
state_dict.update({state_names[i]: state_labs[i] for i in range(len(state_names))})

#--------------------------------------------------------------------
# Ahocorasick Initialization
#--------------------------------------------------------------------
search_terms = (state_names + state_abbv)

auto = ahocorasick.Automaton()

# Add state terms to Aho-Korasick mapping object
for substr in search_terms:
    auto.add_word(substr, substr)
auto.make_automaton()

#--------------------------------------------------------------------
# Ahocorasick Search Functions
#--------------------------------------------------------------------

def AC_search(strings):
    # Initialize empty matches list
    matches = [''] * len(strings)

    for i, astr in enumerate(strings):
        matches[i] = ''
        # If match found, access label via dictionary
        for _, found in auto.iter(astr):
            matches[i] = state_dict[found]
    
    return matches

def tweet_search(tweets, df):
    matches = AC_search(tweets)

    df['state'] = matches
    df = df.loc[np.array(matches) != '']
    df = df.drop(['urls', 'profile_location', 'geotag_location', 'geotag_country'], axis=1)
    return df

#--------------------------------------------------------------------
# Abstracted Geolocate Tweets Function
#--------------------------------------------------------------------

def Geolocate_Tweets(df):
    tweet_loc = df['profile_location'].values

    geolocated_tweets = tweet_search(list(tweet_loc), df)

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