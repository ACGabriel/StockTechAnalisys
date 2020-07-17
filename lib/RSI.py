import numpy as np
import pandas_datareader.data as web
import os

# function calculates RSI
def RSI(prices,n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta=deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            downval = -delta
            upval = 0.
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi

def printCurrentRSI(stock, START, END):
    dfStock = web.DataReader(stock, 'yahoo', START, END)
    rsiStock = RSI(dfStock['Close'])
    print('{} RSI = {}'.format(stock, rsiStock[-1]))

def AnalyseStockRSI(myStocks, wishList):
    print('My Stocks:')
    for myStock in myStocks:
        printCurrentRSI(myStock)

    print('\nWish List Stocks:')
    for wishStock in wishList:
        printCurrentRSI(wishStock)

# function creates list of stocks with RSI between 30-35
def StockLowRSI(START, END):
    try:
        if not os.path.isfile('OSBListLowRSI.txt'):
            newFile = open("OSBListLowRSI.txt", 'x')
        newFile = open("OSBListLowRSI.txt", "w")

        with open('OSBListOL.txt') as fp:
            for stock in fp.read().splitlines():
                stock.rstrip('\n')
                if (stock!= 'EMAS.OL'):
                    print(stock)
                    df = web.DataReader(stock, 'yahoo', START, END)
                    rsi = RSI(df['Close'])
                    if (rsi[-1] > 36.0)  and (rsi[-1] <41.0) and (df['Close'][-1]>10):
                        newFile.write(stock + '\n')
    finally:
        fp.close()