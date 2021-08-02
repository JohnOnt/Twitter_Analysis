import pandas as pd
import numpy as np
import os
import sys
import glob



# This script takes three arguments year (ex. 2020), month (ex. 3), keyterm in all caps (ex. ALCOHOL)

#--------------------------------------------------------------------
# Search Functions
#--------------------------------------------------------------------

def word_search(word, text, df):

    ind = np.char.find(np.char.upper(text), word)
    ind[ind >= 0] = 1
    ind[ind == -1] = 0

    return df.loc[ind.astype('bool')]


if __name__ == "__main__":

    year    = str(sys.argv[1])
    month   = str(sys.argv[2])
    keyterm = str(sys.argv[3])
    
    #print(keyterm)
    #text = ['DeWine says he has no answers on whether COVID-19 spread has been related to protest, but he encourages that the question be asked again soon and thinks he may have more data eventually.']
    #print(np.char.find(np.char.upper(text), keyterm))

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

        day_tweets_kw = word_search(keyterm, tweet_text, day_tweets)
        tweet_count_kw += day_tweets_kw.shape[0]
        li.append(day_tweets_kw)

    month_tweets_kw = pd.concat(li, axis=0, ignore_index=True)

    print('Total tweets: ', tweet_count)
    print('Total tweets kw: ', tweet_count_kw)
    #--------------------------------------------------------------------
    # Write Tweets 
    #--------------------------------------------------------------------

    # Strip to remove whitespace
    write_dir = '/media/johnattan/LaCie/Twitter_Terms/' + keyterm.strip() + '/' 

    # Create directory if it does not already exist
    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    month_tweets_kw.to_csv(write_dir + year + '-' + month + '.csv')
