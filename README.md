# File descriptions

## keyword_extracy.py (year, month, keyword)

Extracts all tweets containing passed keyword for specified month of tweet data.

# keyword_remove.py (year, month, keyword)

Removes all isntances of keyword from data collected in *keyword_extract* script.
This is useful for cases such as ALCOHOL minus SANITIZER related tweets.

## count_states.py (year, month)

Counts the total tweets per identifiable state for a given date.
The data generated is generally used as a reference for total Covid-related tweet volume.

