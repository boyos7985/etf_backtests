
#Financial_tools.py

# calc max drawdown
import numpy as np
import pandas as pd
import math


def GetMaxDrawdown(myDF_PnL_cumprod):
    
    # Assuming myDF_PnL_cumprod is your cumulative product series

    # Step 1: Calculate Running Max
    
    running_max=myDF_PnL_cumprod.cummax()
    
    drawdown=running_max-myDF_PnL_cumprod
    
    myMaxDrawdownPct=drawdown/running_max
    
    GetMaxDrawdown=myMaxDrawdownPct.max()
    
    return GetMaxDrawdown

def GetYearlyRate(FV,StartDate,EndDate):
    from datetime import datetime
    
    StartDate=datetime.strptime(StartDate, '%Y-%m-%d')
    EndDate=datetime.strptime(EndDate, '%Y-%m-%d')
    
    myT=(EndDate-StartDate).days/365.0
    res=math.exp(math.log(FV)/myT)-1
    return res




def turningLong_or_Flat_AssetExit(df, Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on,consDays,DaysExit=None):
    # function that makes you hold asset  by implementing booleans
    # working for S&P, asset 2 and 3
    if DaysExit is None:
        DaysExit=consDays
    
    required_columns=[Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f'Column {column} not found in DataFRame.')
    if not isinstance(consDays, int) or consDays <= 0:
        raise ValueError("consDays must be a positive integer.")
    
    # checking if prices above MA
    is_above_MA=0
    is_above_MA=df[Asset_Base_0]>df[MA_200_Asset_Base_0]
    is_above_MA=is_above_MA.astype(int)
    consecutive_days=0
    consecutive_days=is_above_MA.astype(int).rolling(window=consDays).sum()== consDays
    consecutive_days=consecutive_days.astype(int)

    is_below_MA=0
    is_below_MA=df[Asset_Base_0]<df[MA_200_Asset_Base_0]
    is_below_MA=is_below_MA.astype(int)
    consecutive_daysBelow=0
    consecutive_daysBelow=is_below_MA.astype(int).rolling(window=DaysExit).sum()== DaysExit
    consecutive_daysBelow=consecutive_daysBelow.astype(int)
    
    df[Bool_asset_on]=0

    # Case 1: Activate Bool_asset_on if not previously held and conditions are met
    df.loc[(df[Bool_asset_on].shift(1) == 0) & (consecutive_days== 1),Bool_asset_on] = 1

    # For Case 2, use rolling to count '1's over the last X days for both conditions
    rolling_is_above_MA = is_above_MA.shift().rolling(window=DaysExit).apply(lambda x: (x >= 1).sum(), raw=True)
    rolling_consecutive_days = consecutive_days.shift().rolling(window=DaysExit).apply(lambda x: (x >= 1).sum(), raw=True)


    
    # Case 2: Continuation - Held before and conditions are still met
    # This checks if either condition has been met at least once in the last 5 days
    continuation_condition = ((rolling_is_above_MA >= 1) | (rolling_consecutive_days >= 1)).astype(int)

    # Apply continuation condition where 'Bool Tsylev3 On' was previously 1
    # This checks if either condition has been met at least once in the last 5 days
    # df.loc[df['Bool Tsylev3 On'].shift(1) == 1, 'Bool Tsylev3 On'] = continuation_condition

    
    
    for i in range(1,len(df)-1):
        if (df[Bool_asset_on].iloc[i-1]==1) & (continuation_condition.iloc[i]==1):
            df[Bool_asset_on].iloc[i]=1
    
    for i in range(1,len(df)-1):
        if (df[Bool_asset_on].iloc[i-1]==1) & (consecutive_daysBelow.iloc[i]==1):
            df[Bool_asset_on].iloc[i]=0
    
    # rolling_is_above_MA.to_csv('rollAbovMA.csv')
    # rolling_consecutive_days.to_csv('roll consDays.csv')
    df['rolling_is_above_MA_'+Asset_Base_0]=rolling_is_above_MA
    df['rolling_consecutive_days'+Asset_Base_0]=rolling_consecutive_days
    df['continuation_condition'+Asset_Base_0]=continuation_condition
    # test booleans                   
    
    return df

def turningLong_or_Flat_Asset(df, Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on,consDays,DaysExit=None):
    # function that makes you hold asset  by implementing booleans
    # working for S&P, asset 2 and 3
    if DaysExit is None:
        DaysExit=consDays
    
    required_columns=[Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f'Column {column} not found in DataFRame.')
    if not isinstance(consDays, int) or consDays <= 0:
        raise ValueError("consDays must be a positive integer.")
    
    # checking if prices above MA
    is_above_MA=0
    is_above_MA=df[Asset_Base_0]>df[MA_200_Asset_Base_0]
    is_above_MA=is_above_MA.astype(int)
    consecutive_days=0
    consecutive_days=is_above_MA.astype(int).rolling(window=consDays).sum()== consDays
    consecutive_days=consecutive_days.astype(int)
    df[Bool_asset_on]=0

    # Case 1: Activate Bool_asset_on if not previously held and conditions are met
    df.loc[(df[Bool_asset_on].shift(1) == 0) & (consecutive_days== 1),Bool_asset_on] = 1

    # For Case 2, use rolling to count '1's over the last X days for both conditions
    rolling_is_above_MA = is_above_MA.shift().rolling(window=DaysExit).apply(lambda x: (x >= 1).sum(), raw=True)
    rolling_consecutive_days = consecutive_days.shift().rolling(window=DaysExit).apply(lambda x: (x >= 1).sum(), raw=True)


    
    # Case 2: Continuation - Held before and conditions are still met
    # This checks if either condition has been met at least once in the last 5 days
    continuation_condition = ((rolling_is_above_MA >= 1) | (rolling_consecutive_days >= 1)).astype(int)

    # Apply continuation condition where 'Bool Tsylev3 On' was previously 1
    # This checks if either condition has been met at least once in the last 5 days
    # df.loc[df['Bool Tsylev3 On'].shift(1) == 1, 'Bool Tsylev3 On'] = continuation_condition
    for i in range(1,len(df)-1):
        if (df[Bool_asset_on].iloc[i-1]==1) & (continuation_condition.iloc[i]==1):
            df[Bool_asset_on].iloc[i]=1

    # rolling_is_above_MA.to_csv('rollAbovMA.csv')
    # rolling_consecutive_days.to_csv('roll consDays.csv')
    df['rolling_is_above_MA_'+Asset_Base_0]=rolling_is_above_MA
    df['rolling_consecutive_days'+Asset_Base_0]=rolling_consecutive_days
    df['continuation_condition'+Asset_Base_0]=continuation_condition
    # test booleans                   
    
    return df



def turningLong_or_Flat_Asset_conditional_2_refAsset(df, Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on,Bool_asset_ref,consDays):
# function that makes you hold asset when the Bool_asset_ref is not hold
# working for treasury


    required_columns=[Asset_Base_0,MA_200_Asset_Base_0,Bool_asset_on,Bool_asset_ref]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f'Column {column} not found in DataFrame')
    if not isinstance(consDays, int) or consDays <= 0:
        raise ValueError("consDays must be a positive integer.")

    # checking if prices above MA
    is_above_MA=0
    is_above_MA=df[Asset_Base_0]>df[MA_200_Asset_Base_0]
    is_above_MA=is_above_MA.astype(int)
    consecutive_days=0
    consecutive_days=is_above_MA.astype(int).rolling(window=consDays).sum()== consDays
    consecutive_days=consecutive_days.astype(int)
    df[Bool_asset_on]=0

    # Case 1: Activate Bool_asset_on if not previously held bool_asset_ref=0 and conditions are met
    df.loc[(df[Bool_asset_on].shift(1) == 0) & (consecutive_days== 1) & (df[Bool_asset_ref]==0),Bool_asset_on] = 1

    # For Case 2, use rolling to count '1's over the last 5 days for both conditions
    rolling_is_above_MA = is_above_MA.shift().rolling(window=consDays).apply(lambda x: (x >= 1).sum(), raw=True)
    rolling_consecutive_days = consecutive_days.shift().rolling(window=consDays).apply(lambda x: (x >= 1).sum(), raw=True)

    # Case 2: Continuation - Held before and conditions are still met
    # This checks if either condition has been met at least once in the last 5 days
    continuation_condition = (((rolling_is_above_MA >= 1) | (rolling_consecutive_days >= 1)) & (df[Bool_asset_ref]==0)).astype(int)

    # Apply continuation condition where 'Bool Tsylev3 On' was previously 1
    # This checks if either condition has been met at least once in the last 5 days
    # df.loc[df['Bool Tsylev3 On'].shift(1) == 1, 'Bool Tsylev3 On'] = continuation_condition
    for i in range(1,len(df)-1):
        if (df[Bool_asset_on].iloc[i-1]==1) & (continuation_condition.iloc[i]==1):
            df[Bool_asset_on].iloc[i]=1

    # rolling_is_above_MA.to_csv('rollAbovMA.csv')
    # rolling_consecutive_days.to_csv('roll consDays.csv')
    df['rolling_is_above_MA_'+Asset_Base_0+Bool_asset_ref]=rolling_is_above_MA
    df['rolling_consecutive_days'+Asset_Base_0+Bool_asset_ref]=rolling_consecutive_days
    df['continuation_condition'+Asset_Base_0+Bool_asset_ref]=continuation_condition

    return df

def RSi(df,PxChangeColumn,Asset_name,window):
    
    required_columns=[PxChangeColumn,Asset_name]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f'Column {column} not found in DataFrame')
    dftemp=pd.DataFrame()
    # Separate gains and losses
    dftemp['Gain'] = df[PxChangeColumn].where(df[PxChangeColumn] > 0, 0)
    dftemp['Loss'] = -df[PxChangeColumn].where(df[PxChangeColumn] < 0, 0)

    # Calculate average gain and loss
    window = 14
    avg_gain = dftemp['Gain'].rolling(window=window, min_periods=1).mean()
    avg_loss = dftemp['Loss'].rolling(window=window, min_periods=1).mean()

    # Calculate RS
    rs = avg_gain / avg_loss
    
    RSIcolumn_name='RSI_'+Asset_name
    # Calculate RSI
    df[RSIcolumn_name] = 100 - (100 / (1 + rs))
    
    return df

def z_score(data,days):
# gets the zscore, so if you are 190cm high, the zscore might be 2.5 ie you are 2.5std away from the mean height
# can use:
# rolled.plot()
# rolled.hist(bins=20)
    rolling_mean=data.rolling(window=days).mean()
    rolling_std=data.rolling(window=days).std()
    return (data-rolling_mean)/rolling_std

def Realized_vol(data,period):
#     mu=avg
# we assume we calc based on net return, else add div
    log_returns=np.log(data/data.shift(1))
    mu=log_returns.rolling(window=period).mean()
    mu.dropna(inplace=True)
    
    squared_deviations=(log_returns-mu)**2
    
    vol=0
    vol=np.sqrt(squared_deviations.rolling(window=period).sum()/period)
    
    vol=vol*(250**0.5)*100
    
    return vol

# def __main__:
#     startDate='2000-01-01'
#     endDate='2024-01-01'
    
#     myR=GetYearlyRate(4.28,startDate,endDate)
#     print(myR)
    
# if __name__=='__main__':
#     __main__()
