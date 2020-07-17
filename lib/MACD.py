import pandas as pd

# MACD for ewm built-in function
def ComputeMACD(data, slow=26, fast=12):
    '''
    macd line = 12ema - 26ema
    signal line = 9ema of the macd line
    histogram = macd line - signal line
    '''
    emaSlow = pd.Series.ewm(data, span=slow).mean()
    emaFast = pd.Series.ewm(data, span=fast).mean()
    return emaSlow, emaFast, emaFast-emaSlow
