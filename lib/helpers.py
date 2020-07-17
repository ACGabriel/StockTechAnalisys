import os

# function is adding '.OL' to the short name of stock from file 'OSBList.txt'
def AddOL():
    try:
        if not os.path.isfile('OSBListOL.txt'):
            newFile = open("OSBListOL.txt", 'x')
        newFile = open("OSBListOL.txt", "w")
        with open('OSBList.txt') as fp:
            for line in fp.read().splitlines():
                line.rstrip('\n')
                newFile.write(line+'.OL\n')

    finally:
        fp.close()
        newFile.close()

def AnalyseStockDailyOHLC(stockDF):
    stockDF['diffHL'] = stockDF['High'] - stockDF['Low']
    stockDF['diffOH'] = stockDF['Open'] - stockDF['High']
    stockDF['diffOC'] = stockDF['Open'] - stockDF['Low']
    # print(stockDF[['Open', 'High', 'Low', 'Close', 'diffHL', 'diffOH', 'diffOC']].tail(30))
    try:
        if not os.path.isfile('OSBDailyAnalysis.csv'):
            newFile = open("OSBDailyAnalysis.csv", 'x')
        newFile = open("OSBDailyAnalysis.csv", "w")
        stockDF.tail(30).to_csv(newFile, sep='\t', columns=['Open', 'High', 'Low', 'Close', 'diffHL', 'diffOH', 'diffOC'], encoding='utf-8')
    finally:
        newFile.close()