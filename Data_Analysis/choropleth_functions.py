import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

state_labs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#------------------------------------------------------------------
# Helper Functions 
#------------------------------------------------------------------

def fetch_data_kw(kw):
    dir = '/media/johnattan/LaCie/Twitter_Terms/' + kw + '/GEO-Tweets.csv'
    df = pd.read_csv(dir, index_col=None, header=0)
    df = df.drop(labels = ['Unnamed: 0', 'Unnamed: 0.1', 'id'], axis = 1)

    return df

def fetch_data_cts(date):
    dir = '/media/johnattan/LaCie/Twitter_Terms/State_Counts/' + date + '.csv'
    df = pd.read_csv(dir, index_col=None, header=0)
    
    return df

def collapse_count(df):
    states = []
    counts = []
    for state in df.State.unique():
        states.append(state)
        counts.append(np.sum(df[df.State == state].Counts))
    
    collapsed_cts = pd.DataFrame([])
    collapsed_cts['State'] = states
    collapsed_cts['Count'] = counts
    
    return collapsed_cts

def subset_date(df, date):
    inds = [x[0:7] == date for x in df.created_at.values]   
    
    return df[inds]

def count_by_state(df):
    counts = df.state.value_counts()
    
    # Fill zero states
    zero_states = list(set(state_labs) - set(list(counts.index.values)))
    
    for state in zero_states:
        counts = counts.append(pd.Series([0], index=[state]))
    
    return counts


def build_dataframe(kw, dates, waves = False, write_data = False):
    
    df_kw = fetch_data_kw(kw)
    
    dfs = []
    
    for date in dates:
        df_kw_date = subset_date(df_kw, date)
        kw_cts = count_by_state(df_kw_date)

        df_cts = collapse_count(fetch_data_cts(date))
        kw_cts = kw_cts.sort_index()
        
        dfs.append(pd.DataFrame({'State': kw_cts.index.values, 'Date': date,'Count' : kw_cts.values / df_cts.Count.values}))

    if waves:
        df = pd.concat(dfs, axis=0, ignore_index=True)
        

        pass

    df = pd.concat(dfs, axis=0, ignore_index=True)

    if write_data:
        df.to_csv('Train_Data/' + kw + '-' + dates[0] + '--' + dates[-1] + '.csv')

    return df

#------------------------------------------------------------------
# Plotting Functions 
#------------------------------------------------------------------

def plotty(kw, date, renderer = 'png'): 
    state_count = build_dataframe(kw, [date])

    fig = go.Figure(data=go.Choropleth(
        locations=state_count.State, # Spatial coordinates
        z = state_count.Count, # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        #colorbar_title = "Tweet Counts / Tweet Volume",
        zmin = 0,
        zmax = max(state_count['Count']),
        colorbar_title = "tweets"
    ))

    if kw == '':
        fig.update_layout(
            title_text = 'Tweets related to Covid-19',
            geo_scope='usa', # limite map scope to USA
        )
    else:
        fig.update_layout(
            title_text = 'Tweets related to Covid-19 and ' + kw + ' ' + date,
            geo_scope='usa', # limite map scope to USA
        )
    fig.show(renderer = renderer)
    fig.write_image('figures/' + kw + '/' + kw + '-' + date + '.png')
    fig.write_html('figures/' + kw + '/' + kw + '-' + date + '.html')

def plotty_plots(kw, dates, renderer = 'png', rows = 2, cols = 3, savefig = False):
    state_count = build_dataframe(kw, dates)

    Months = pd.DataFrame({'2020-01': '2020-01', '2020-02': '2020-02', '2020-03': '2020-03', 
                           '2020-04': '2020-04', '2020-05': '2020-05', '2020-06': '2020-06',
                           '2020-07': '2020-07', '2020-08': '2020-08', '2020-09': '2020-09',
                           '2020-10': '2020-10', '2020-11': '2020-11', '2020-12': '2020-12'}, index=[0])
    
    Months = Months[dates]
     
    fig = make_subplots(
        rows=rows, cols=cols,
        specs = [[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)],
        subplot_titles = list(Months.loc[0,:]))
    
    for i, month in enumerate(Months):
        result = state_count[['State', 'Count']][state_count.Date == month]
        fig.add_trace(go.Choropleth(
            locations=result.State,
            z = result.Count,
            locationmode = 'USA-states', # set of locations match entries in `locations`
            marker_line_color='white',
            zmin = 0,
            zmax = max(state_count['Count']),
            colorbar_title = "tweets",
        ), row = i//cols+1, col = i%cols+1)

    fig.update_layout(
        title_text = 'Tweets related to Covid-19 and ' + kw,
        **{'geo' + str(i) + '_scope': 'usa' for i in [''] + np.arange(2,rows*cols+1).tolist()},
        )

    fig.show(renderer = renderer)
    if savefig:
        fig.write_image('figures/' + kw + '/' + kw + '-' + dates[0] + '--' + dates[-1] + '.png')
        fig.write_html('figures/' + kw + '/' + kw + '-' + dates[0] + '--' + dates[-1] + '.html')


    
def plotty_plots_w(kw, dates, renderer = 'png', rows = 1, cols = 3, savefig = False):
    state_count = build_dataframe(kw, dates)
    # Standardize, currently off
    #state_count['Count'] = (state_count.Count-state_count.Count.min())/(state_count.Count.max()-state_count.Count.min())

    Wave_names = ['Wave 1', 'Wave 2', 'Wave 3']  
    Wave_dates = [['2020-01', '2020-02'], ['2020-03', '2020-04'], ['2020-05', '2020-06']]

    li = []

    for wave in Wave_dates:
        result = pd.concat([state_count[['State', 'Count']][state_count.Date == wave[0]], 
                            state_count[['State', 'Count']][state_count.Date == wave[1]]], 
                            axis=0, ignore_index=True)

        result = result.groupby('State').mean()

        li.append(result)

    state_count = pd.concat(li, axis=0, ignore_index=True)
     
    fig = make_subplots(
        rows=rows, cols=cols,
        specs = [[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)],
        subplot_titles = Wave_names)
    
    for i, result in enumerate(li):


        fig.add_trace(go.Choropleth(
            locations=result.index.values,
            z = result.Count,
            locationmode = 'USA-states', # set of locations match entries in `locations`
            marker_line_color='white',
            zmin = 0,
            zmax = max(state_count['Count']),
            colorbar_title = "tweets",
        ), row = i//cols+1, col = i%cols+1)

    fig.update_layout(
        title_text = 'Tweets related to Covid-19 and ' + kw,
        **{'geo' + str(i) + '_scope': 'usa' for i in [''] + np.arange(2,rows*cols+1).tolist()},
        )

    fig.show(renderer = renderer)
    if savefig:
        fig.write_image('figures/' + kw + '/' + dates[0] + '--' + dates[-1] + '_waves.png')



def plotty_w(kw, wave, renderer = 'png'): 

    Wave_dates = {'1': ['2020-01', '2020-02'], '2':['2020-03', '2020-04'], '3':['2020-05', '2020-06']}
    dates = Wave_dates[wave]

    state_count = build_dataframe(kw, dates)

    state_count = pd.concat([state_count[['State', 'Count']][state_count.Date == dates[0]], 
                        state_count[['State', 'Count']][state_count.Date == dates[1]]], 
                        axis=0, ignore_index=True)
    
    state_count = state_count.groupby('State').mean()
    # state_count['Count'] = (state_count.Count-state_count.Count.min())/(state_count.Count.max()-state_count.Count.min())

    fig = go.Figure(data=go.Choropleth(
        locations=state_count.index.values, # Spatial coordinates
        z = state_count.Count, # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        #colorbar_title = "Tweet Counts / Tweet Volume",
        zmin = 0,
        zmax = max(state_count['Count']),
        colorbar_title = "tweets"
    ))

    fig.update_layout(
        title_text = 'Tweets related to Covid-19 and ' + kw + ' Wave: ' + wave,
        geo_scope='usa', # limit map scope to USA
    )
    fig.show(renderer = renderer)
    fig.write_image('figures/' + kw + '/' + 'waves' + '-' + wave + '.png')