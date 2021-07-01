import pandas as pd
import numpy as np
import glob
import sys



state_labs = np.array(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

state_abbv = np.array([", AL", ", AK", ", AZ", ", AR", ", CA", ", CO", ", CT", ", DC", ", DE", ", FL", ", GA", 
          ", HI", ", ID", ", IL", ", IN", ", IA", ", KS", ", KY", ", LA", ", ME", ", MD", 
          ", MA", ", MI", ", MN", ", MS", ", MO", ", MT", ", NE", ", NV", ", NH", ", NJ", 
          ", NM", ", NY", ", NC", ", ND", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", 
          ", SD", ", TN", ", TX", ", UT", ", VT", ", VA", ", WA", ", WV", ", WI", ", WY"])

state_names = np.array(["Alabama", "Alaska", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",  
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",  
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"])

#search_terms = np.append(state_names, state_abbv)

#--------------------------------------------------------------------
# Subset times to when US users most active
#--------------------------------------------------------------------

def strip_time(x):
    return x[11:13]

def subset_time(df):
    time_vec = df.created_at.values
    df['hour'] = int(np.vectorize(strip_time)(time_vec))

    return df[(df.hour > 15) & (df.hour < 22)]

#--------------------------------------------------------------------
# Search Functions
#--------------------------------------------------------------------

def state_search(state, text):
    ind = np.char.find(np.char.upper(text), np.char.upper(state))
    ind[ind >= 0] = 1
    ind[ind == -1] = 0
    return np.sum(ind)

def states_search(text):
    lst = np.array([state_labs[state_names == state][0] if state_search(state, text) > 0 else '' for state in state_names])
    lst = np.append(lst, np.array([state_labs[state_abbv == state][0] if state_search(state, text) > 0 else '' for state in state_abbv]))
    lst = lst[lst != '']

    if len(lst) > 0:
        return lst[0]
    
    else:
        return ''

def tweet_search(tweets, df):
    matches = np.vectorize(states_search)(tweets)

    df['state'] = matches
    df = df.loc[matches != '']
    df = df.drop(['urls', 'profile_location', 'geotag_location', 'geotag_country'], axis=1)
    return df

#--------------------------------------------------------------------
# Abstracted Geolocate Tweets Function
#--------------------------------------------------------------------

def Geolocate_Tweets(df):
    tweet_loc = df['profile_location'].values
    tweet_loc = tweet_loc.astype('<U40')

    geolocated_tweets = tweet_search(tweet_loc, df)

    print("In Rows: ", df.shape[0])
    print("Out Rows: ", geolocated_tweets.shape[0])

    return geolocated_tweets

#--------------------------------------------------------------------
# Count Tweets by State 
#--------------------------------------------------------------------

def count_state_tweets(df, day):

    counts = df.state.value_counts()
    state_counts = pd.DataFrame([])
    state_counts['State'] = counts.sort_index().index
    state_counts['Counts' + str(day)] = counts.sort_index().values 

    return state_counts

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        year    = str(sys.argv[1])
        month   = str(sys.argv[2])
    
    else:
        print("Debug Mode Active")
        year = 2020
        month = 2

    #--------------------------------------------------------------------
    # Now has to be broken up into separate files and slowly compiled
    #--------------------------------------------------------------------

    data_dir = '/media/johnattan/LaCie/Twitter_Data_Adam/' + year + '/' + month + '/' 
    all_files = glob.glob(data_dir + "*.csv")

    li = []

    for filename in all_files:
        print('On file: ', filename)
        day_tweets = pd.read_csv(filename, index_col=None, header=0)
        day_tweets = day_tweets.dropna(subset = ['profile_location', 'text'])

        geo_tweets = Geolocate_Tweets(day_tweets)

        li.append(count_state_tweets(geo_tweets, filename[-5]))

