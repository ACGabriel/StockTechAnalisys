import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
import pandas_datareader.data as web
import matplotlib
import sys

sys.path.insert(0, './lib')
from plotZoomMouseWhell import pre_zoom, re_zoom
from RSI import RSI, printCurrentRSI, AnalyseStockRSI, StockLowRSI
from exponentialMovingAverage import ExponentialMovingAverage
from MACD import ComputeMACD
# from helpers import AddOL
from plotDrawing import plotDrawing
from stockDataAnalysis import stockDataAnalysis
from dataAnalysis import dataAnalysis

matplotlib.rcParams.update({'font.size':9})

START= dt.date.today() - dt.timedelta(365*2)
END = dt.date.today()-dt.timedelta(0)

# Main Program

myStocks=['FKRAFT.OL','DNB.OL','Bouvet.OL', 'STB.OL', 'MEDI.OL']
wishList = ['TOM.OL', 'TEL.OL', 'GJF.OL', 'NEL.OL']

# print('Start date: {}, end date: {}'.format(start, end))
# stock = 'FKRAFT.OL'
# stock = 'MEDI.OL'
# stock = 'Bouvet.OL'
# stock = 'AKERBP.OL'
# stock = 'DNB.OL'
# stock = 'NEL.OL'
# stock = '^GSPC'
# stock = 'KVAER.OL'
# stock = 'STB.OL'
# stock = 'DNO.OL'
# stock = 'GJF.OL'
# stock = 'TEL.OL'
# stock = 'HEX.OL'
# stock = 'KIT.OL'
# stock = 'TOM.OL'
# stock = 'WWI B.OL'
stock = 'STB.OL'

df = web.DataReader(stock, 'yahoo', START, END)

df = stockDataAnalysis(df)

# df_OSEBX = web.DataReader('OSEBX.OL', 'yahoo', start, end)

# AddOL() # needed only if there are changes for Oslo Stock Exchange list
# StockLowRSI(START, END) # lists stocks with RSI lower 36 and price over 10 NOK
# AnalyseStockRSI(myStocks, wishList)

# plotDrawing(df, stock, END)
dataAnalysis(df, START, END)



