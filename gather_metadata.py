import pandas as pd
import numpy as np
import glob
import sys



# time_vec = unmatched.created_at.values
# #time_vec[2000][11:13]

# def strip_time(x):
    # return x[11:13]

# np.vectorize(strip_time)(time_vec)


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


def count_state_tweets_fast():

    pass


if __name__ == "__main__":
    year    = str(sys.argv[1])
    month   = str(sys.argv[2])

    #--------------------------------------------------------------------
    # Now has to be broken up into separate files and slowly compiled
    #--------------------------------------------------------------------

    data_dir = '/media/johnattan/LaCie/Twitter_Data_Adam/' + year + '/' + month + '/' 
    all_files = glob.glob(data_dir + "*.csv")

    # Keep track of how many tweets there are total and the number containing the key term
    tweet_count = 0
    tweet_count_kw = 0

    li = []
    month_tweets_kw = pd.DataFrame(columns = ['id', 'text', 'created_at', 'urls', 'profile_location',
        'geotag_location', 'geotag_country'])


    for filename in all_files:
        pass