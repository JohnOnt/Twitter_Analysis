import pandas as pd
import numpy as np
import os
import sys
import glob
import pickle


# This script takes three arguments year (ex. 2020), month (ex. 3), keyterm in all caps (ex. ALCOHOL)


#--------------------------------------------------------------------
# Search Functions
#--------------------------------------------------------------------

def word_search_ind(word, text, df, flip=False):
    # Flip var added for the use of getting indices where the keyerm is absent
    ind = np.char.find(np.char.upper(text), word)

    if flip:
        ind[ind >= 0] = 0
        ind[ind == -1] = 1

    else:
        ind[ind >= 0] = 1
        ind[ind == -1] = 0

    return df.index[ind.astype('bool')].values

if __name__ == "__main__":

    year    = str(sys.argv[1])
    month   = str(sys.argv[2])
    keyterm = str(sys.argv[3])
    flip = str(sys.argv[4]) == "True"
    
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
        print('On file: ', filename)
        day_tweets = pd.read_csv(filename, index_col=None, header=0)
        day_tweets = day_tweets.dropna(subset = ['profile_location', 'text'])

        tweet_count += day_tweets.shape[0]

        #--------------------------------------------------------------------
        # Parse Tweets for Key Term
        #--------------------------------------------------------------------

        # Vectorize tweet column and set it to numpy string to optimize speed
        tweet_text = day_tweets['text'].values
        tweet_text = tweet_text.astype('<U140')

        day_inds = word_search_ind(keyterm, tweet_text, day_tweets, flip=flip)
        # Append list of indices
        li.append(day_inds)

    print('Total tweets: ', tweet_count)
    print('Total tweets kw: ', tweet_count_kw)

    # Cannot write a dataframe with different lengths for column so just pickling list object
    write_dir = '/media/johnattan/LaCie/Twitter_Terms/indices/' 

    # Create directory if it does not already exist
    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    pickle.dump(li, open(write_dir + keyterm + "-" + month +  "-" + str(flip) + ".p", "wb" ))



