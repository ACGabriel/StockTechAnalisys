import requests
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from io import StringIO
import csv
from sklearn.impute import SimpleImputer
import os.path

def dataAnalysis(df_stock, START, END):
        
    #  dataset preparation
    print(df_stock.tail())
    
    df = df_stock
    
    
    df_SP500 = web.DataReader('^GSPC', 'yahoo', START, END)
    # print(df_SP500.tail())
    
    df['SP500'] = df_SP500['Adj Close']
    
    df_USDNOK = web.DataReader('USDNOK=X', 'yahoo', START, END)
    # print(df_USDNOK.tail())
    
    
    df['USDNOK'] = df_USDNOK['Adj Close']
    
    print(df.tail())
    
    # getting interest rate data from Norges Bank 
    url = 'https://data.norges-bank.no/api/data/IR/B.KPRA..?format=csv&startPeriod={start}&endPeriod={end}&locale=en'.format(start = START, end = END)
    
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
    req = requests.get(url, headers=headers)
    data = StringIO(req.text)
    # print(req.text)
    
    df_NorgesBankRate = pd.read_csv(data, delimiter=';') #, usecols=[11,12], index_col=[11]
    print(df_NorgesBankRate.columns)
    df_NorgesBankRate.columns = df_NorgesBankRate.iloc[0]
    df_NorgesBankRate['TIME_PERIOD'] = pd.to_datetime(df_NorgesBankRate['TIME_PERIOD'])
    
    df.set_index('TIME_PERIOD', inplace=True)
    
    df_NorgesBankRate = df_NorgesBankRate.iloc[:, 11:-2];
    df_NorgesBankRate.index.names = ['Date']
    # df_NorgesBankRate.rename(columns = {'OBS_VALUE':'KPRA'})
    print(df_NorgesBankRate['OBS_VALUE'].tail())
    # df['KPRA'] = df_NorgesBankRate['OBS_VALUE']
    
    print(df.tail())
    
    
    # taking care of missing data
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(df)
    df = imputer.transform(df)
    print(df.tail())
    
    createFilesFromDatasets(df_SP500, df_USDNOK, df_NorgesBankRate, df)
    
def createFilesFromDatasets(df_SP500, df_USDNOK, df_NorgesBankRate, df):
    # if files exsist, then delete
    if os.path.isfile('USDNOK.xls'):
        os.remove("USDNOK.xls")
    if os.path.isfile('SP500.xls'):
        os.remove("SP500.xls")
    if os.path.isfile('Main.xls'):
        os.remove("Main.xls")
    if os.path.isfile('NorgesBankRate.xls'):
        os.remove("NorgesBankRate.xls")
    
    # create files
    df_SP500.to_excel('SP500.xls')
    df_USDNOK.to_excel('USDNOK.xls')
    df_NorgesBankRate.to_excel('NorgesBankRate.xls')
    df.to_excel('Main.xls')