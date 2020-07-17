import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
import matplotlib
from decimal import Decimal
import sys


sys.path.insert(0, './lib')
#from plotZoomMouseWhell import pre_zoom, re_zoom
from MACD import ComputeMACD
from helpers import AnalyseStockDailyOHLC
from RSI import RSI

def plotDrawing(df, stock, END):
    style.use('ggplot')
    
    matplotlib.rcParams.update({'font.size':9})
        
    # Main Chart
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
    ax1.xaxis_date()
    ax1.grid(True)
    
    candlestick_ohlc(ax1,
                     zip(mdates.date2num(df.index.to_pydatetime()),
                             df['Open'], df['High'],
                             df['Low'], df['Close']),
                     colorup='g',
                     colordown='r',
                     width=0.6)
    
    # ax1.plot(df.index, df['10ema'], color='#FF9999')
    # ax1.plot(df.index, df['30ema'], color='#CC0000')
    
    ax1.plot(df.index, df['10ema'], color='#FF9999', label='10ema', lw=1.0, )
    ax1.plot(df.index, df['30ema'], color='#CC0000', label='30ema', lw=1.0, )
    ax1.plot(df.index, df['50sma'], color='#4169E1', label='50sma', lw=1.0, alpha=0.7)
    # ax1.plot(df.index, df['100sma'], color='#6A5ACD', label='100sma', lw=1.0, alpha=0.7)
    # ax1.plot(df.index, df['200sma'], color='#800080', label='200sma', lw=1.0, alpha=0.7)
    ax1.plot(df.index, df['Close'], color='#808080', lw=1.0, alpha=0.7)
    ax1.legend(loc='upper left', ncol=2, fontsize='small', framealpha=None)
    
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    
    # ax1.plot(df.index, df['10emaF'], color='#9999FF')
    # ax1.plot(df.index, df['30emaF'], color='#0000FF')
        
    # volumeMin=0
    
    ax1V = ax1.twinx()
    # ax1V.fill_between(df.index,
    #                   volumeMin,
    #                   df['Volume'],
    #                   facecolor='#00ffe8',
    #                   alpha=.5)
    ax1V.bar(df.index, df['Volume'], color='b', alpha=0.5)
    ax1V.axes.yaxis.set_ticklabels([])
    ax1V.grid(False)
    ax1V.set_ylim(0, 2.5*df['Volume'].max())
    ax1V.tick_params(axis='x', colors='b')
    ax1V.tick_params(axis='y', colors='b')
    
    
    # Fibonachi analysis
    fibStartDate = dt.datetime(2019, 4, 28)
    fibEndDate = END
    maxClosePrice = df['Close'][fibStartDate:fibEndDate].max()
    minClosePrice = df['Close'][fibStartDate:fibEndDate].min()
    # '''23.6%, 38.2%, 50%, 61.8%,'''
    fib236 = (maxClosePrice-minClosePrice)*0.236 + minClosePrice
    fib382 = (maxClosePrice-minClosePrice)*0.382 + minClosePrice
    fib50 = (maxClosePrice-minClosePrice)*0.5 + minClosePrice
    fib618 = (maxClosePrice-minClosePrice)*0.618 + minClosePrice
    
    ax1.axhline(minClosePrice, color = 'r', lw = 0.7, ls='dashed')
    ax1.axhline(fib236, color = '#ff7400', lw = 0.7, ls='dashed') # orange color
    ax1.axhline(fib382, color = 'r', lw = 0.7, ls='dashed')
    ax1.axhline(fib50, color = '#ff7400', lw = 0.7, ls='dashed')
    ax1.axhline(fib618, color = 'r', lw = 0.7, ls='dashed')
    ax1.axhline(maxClosePrice, color = '#ff7400', lw = 0.7, ls='dashed')
    
    ax1.set_yticks([minClosePrice,fib236,fib382,fib50,fib618,maxClosePrice])
        
    # RSI calculation and plot
    rsiColor = '#00ffe8'
    posColor = '#386d13'
    negColor = '#8f2020'
    rsi = RSI(df['Close'])
    
    ax0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, sharex=ax1)
    
    ax0.plot(df.index, rsi, rsiColor, linewidth=1.0 )
    ax0.set_ylim(0,100)
    ax0.axhline(70, color = negColor, lw = 0.5)
    ax0.axhline(30, color = posColor, lw = 0.5)
    ax0.fill_between(df.index, rsi, 70, where=(rsi>=70), facecolor=negColor, edgecolor=negColor)
    ax0.fill_between(df.index, rsi, 30, where=(rsi<=30), facecolor=posColor, edgecolor=posColor)
    ax0.tick_params(axis='x')
    ax0.tick_params(axis='y')
    ax0.text(0.015, 0.95, 'RSI (14)', va='top', fontsize=7, transform=ax0.transAxes)
    ax0.set_yticks([30,70])
    # =============================================================================
    # f = plotZoomMouseWheel(plt, ax0, base_scale = 1.5)
    # =============================================================================
    
    priceLast=Decimal(df['Close'][-1])
    print(priceLast)
    # print(rsi[-1])
    
    plt.suptitle('{} Stock {}'.format(stock, priceLast.quantize(Decimal(10) ** -2)))
        
    # MACD calculation and plot
    ax2=plt.subplot2grid((6,4), (5,0),rowspan=1, colspan=4, sharex=ax1)
    macdColor = '#18f9bd'
    emasSlow, emaFast, macd = ComputeMACD(df['Close'])
    ema9 = pd.Series.ewm(macd, span=9).mean()
    
    ax2.plot(df.index, macd, color='#0b84fd', lw=2)
    ax2.plot(df.index, ema9, color='r', lw=1)
    ax2.fill_between(df.index, macd-ema9, alpha=0.5, facecolor=macdColor)
    ax2.text(0.015, 0.95, 'MACD 12,26,9', va='top', fontsize=7, transform=ax2.transAxes)
    
    # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
    
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    plt.subplots_adjust(left=.10, bottom=.12,right=.93, top=.95, wspace=.20, hspace=0)
    plt.subplots_adjust(left=.10, bottom=.12,right=.93, top=.95, wspace=.20, hspace=0)
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    # attach zoom functions to plot
    # pre_zoom(plt.figure());
    # plt.connect('motion_notify_event', re_zoom)
    # plt.connect('button_release_event', re_zoom)
    
    AnalyseStockDailyOHLC(df)
    plt.show()


