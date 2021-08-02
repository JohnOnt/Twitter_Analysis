import pandas as pd
import glob
import numpy as np

state_labs = np.array(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

state_names = ["Alabama", "Alaska", "Arizona", "Arkansas",
    "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",  
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",  
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

state_dict = {state_names[i]: state_labs[i] for i in range(len(state_labs))}

def merge_dataframes(kw):

    policy_scores = pd.read_csv('Build_Data/State_Policy_Scores.csv')
    filename = glob.glob('Build_Data/' + kw + "*.csv")[0]
    df = pd.read_csv(filename, index_col=0)

    if len(df.columns) > 5:
        print("Looks like this is already merged")

    df['Score'] = [(policy_scores.iloc[np.where(x == policy_scores.STATE)[0][0]].Score) for x in df.State]
    # Build function for testing contiguous dates later
    #df = subset_date(df, dates)
    df = df.groupby('State').mean()


    features = ['State', 'Density', 'White Percent', 'Black Percent', 'Hispanic Percent', "Bachelor's Degree or higher", 'Median household income', 'COVID Cases (% of Population)', 'Peak Unemployment']
    demographics = pd.read_csv('/home/johnattan/Documents/CHIP/GST_Alc/Features_Data - Feature_Data.csv')
    demographics = demographics[features]

    li = []
    for name in demographics.State.values:
        li.append(state_dict[name])
    
    demographics['State'] = li
    final_df = pd.merge(df, demographics, on='State')
    final_df.to_csv('Train_Data/' + filename[11:])


test = merge_dataframes('ALCOHOL')