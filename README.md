# File descriptions

## keyword_extracy.py (year, month, keyword)

Extracts all tweets containing passed keyword for specified month of tweet data.

## keyword_remove.py (year, month, keyword)

Removes all isntances of keyword from data collected in *keyword_extract* script.
This is useful for cases such as ALCOHOL minus SANITIZER related tweets.

## count_states.py (year, month)

Counts the total tweets per identifiable state for a given date.
The data generated is generally used as a reference for total Covid-related tweet volume.


# Data Generation Process
Given a keyword such as 'BEER' to search for:
- *keyword_extract* parses all tweets in available data and writes one csv file per month containing tweets with keyterm
- *us_states_extract* uses these data to do another round of parsing, keeping tweets where the US state is possible to identify via profile_location data
- *keyword_remove* is used to remove corner cases that are not relevant to the study such as ALCOHOL tweets that are related to SANITIZErs
- *count_states* is used to collect the total number of tweets produced by identifiable US state tweets