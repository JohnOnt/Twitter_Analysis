import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV
import matplotlib.pyplot as plt
import glob
import statsmodels.api as sm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

policy_scores = pd.read_csv('State_Policy_Scores.csv')

def get_data(kw, features, dates):
    filename = glob.glob('Train_Data/' + kw + "*.csv")[0]
    df = pd.read_csv(filename, index_col=0)
    df['Score'] = [(policy_scores.iloc[np.where(x == policy_scores.STATE)[0][0]].Score) for x in df.State]

    df = subset_date(df, dates)
    df = df.groupby('State').mean()

    # Add State Demographics
    state_dem = pd.read_csv('/home/johnattan/Documents/CHIP/GST_Alc/Features_Data - Feature_Data.csv')
    #features = ['White Percent', 'Black Percent', 'Hispanic Percent', 'High School Diploma or Higher', "Bachelor's Degree or higher", 'With an Advanced Degree', 'Percent Pop of US', 'Density', 'Average Income', 'Peak Unemployment', 'COVID Cases', 'COVID Deaths', 'Population', 'COVID Cases (% of Population)']

    state_dem.index = df.index.values

    return pd.concat([df, state_dem[features]], axis=1)

def subset_date(df, dates):
    inds = np.zeros(df.shape[0])

    for date in dates:
        tmp_inds = [x[0:7] == date for x in df.Date]   
        inds = inds + 1*np.array(tmp_inds)
    
    return df[list(map(bool,inds))]

def summarize_models(kw, dates, features, verbose=False):
    df = get_data(kw, features, dates)

    X = df[features + ['Score']] 
    X = sm.add_constant(X)

    y =  df.Count.values

    mod = sm.OLS(y, X)
    res = mod.fit()
    if verbose:
        print(res.summary())
    else:
        print("R2: ", np.round(res.rsquared, 3))
        print(list(zip(res.pvalues[res.pvalues < 0.1].index, 
        np.round(res.pvalues[res.pvalues < 0.1].values, 5) )))



def summarize_LASSO(kw, dates, features):
    df = get_data(kw, dates)
    X = df[features] 
    y =  df.Count.values

    lassocv = LassoCV(alphas = None, cv = 10, max_iter = 100000, normalize = True)
    lassocv.fit(X, y)

    print('Optimal alpha: ', lassocv.alpha_)

    # Inference with the optimal model
    model = Lasso(alpha=lassocv.alpha_)
    model.fit(X, y)

    # Print out coefs
    estimates = zip(features, model.coef_)
    for pair in estimates:
        print(pair)


def plot_models(kw, X, y, model):

    #fig, axs = plt.subplots(nrow, ncol, figsize = (20, 5))
    #fig.suptitle(kw + ' Tweet Volume vs State Alcohol Policy Score')
    #fig.subplots_adjust(hspace = .7)
    #axs = axs.ravel()

    # for i, date in enumerate(dates):
        # if wave:
            # df_sub = subset_date_w(df, date)
        # else:
            # df_sub = subset_date(df, date)

        # X = (df_sub.Score.values).reshape(-1,1)
        # y =  df_sub.Count.values

        # reg = LinearRegression().fit(X, y)
        # li.append(pd.DataFrame({'Date': [date], 'Coef': reg.coef_, 'Score': [reg.score(X, y)]}))

    # axs[i].scatter(X, y, c='black') 
    # axs[i].plot(X, reg.predict(X))
    # axs[i].set_title(date)
    # axs[i].set(xlabel='Policy Score', ylabel='Tweet Volume')

    plt.scatter(X, y, c='black')
    plt.plot(X, model.predict(X))
 
    if False:
        if wave:
            fig.savefig('figures/Regression/' + kw + '_waves.png')
        else:
            fig.savefig('figures/Regression/' + kw + '.png')



features_a = ['Density', 'White Percent', 'Hispanic Percent', "Bachelor's Degree or higher", 'Median household income', 'COVID Cases (% of Population)', 'Peak Unemployment']

dates2 = ['2020-03', '2020-04', '2020-05', '2020-06']#, '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12']

summarize_models('ALCOHOL', dates2, features_a)