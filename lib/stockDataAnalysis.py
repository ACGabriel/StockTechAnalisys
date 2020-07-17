import pandas as pd


from RSI import RSI
from exponentialMovingAverage import ExponentialMovingAverage

def stockDataAnalysis(df):
    

    df['5ema'] = pd.Series.ewm(df['Close'], span=5).mean()
    df['10ema'] = pd.Series.ewm(df['Close'], span=10).mean()
    df['21ema'] = pd.Series.ewm(df['Close'], span=21).mean()
    df['30ema'] = pd.Series.ewm(df['Close'], span=30).mean()
    df['50ema'] = pd.Series.ewm(df['Close'], span=50).mean()
    
    df['20sma']=df['Adj Close'].rolling(window=20).mean()
    df['50sma']=df['Adj Close'].rolling(window=50).mean()
    df['100sma']=df['Adj Close'].rolling(window=100).mean()
    df['200sma']=df['Adj Close'].rolling(window=200).mean()
    
    df['10emaF'] = ExponentialMovingAverage(df['Close'], 10)
    df['30emaF'] = ExponentialMovingAverage(df['Close'], 30)
    
    # SP = len(df['Close',200 - 1])
    
    df.dropna(inplace=True)
    
    df["RSI"] = RSI(df['Adj Close'], 14)
    return df