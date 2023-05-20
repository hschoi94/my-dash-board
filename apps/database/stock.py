import pandas as pd
import numpy as np

import os
from pathlib import Path
import FinanceDataReader as fdr
# from pykrx import stock
# import yfinance as yf
# https://hyunyulhenry.github.io/quant_cookbook/금융-데이터-수집하기-기본.html
import os
from .database import DataBase 
import shutil
import datetime

# Ticker,Market,Date,Open,High,Low,Close,Volume,Change
def comp_list_w_list(list_,c_lists_):
    temp = []
    for u in c_lists_:
        if u not in list_:
            temp.append(u)
    return temp

def stock_csv2db(config):
    sql = StockTable(config)
    stock_data_root_path = os.path.abspath(
        "/Users/choehyeongseog/git/service-master-server/stock-files")
    done_path = os.path.join(os.path.dirname(stock_data_root_path), 'done')
    """
    root
     - market
        - ticker
    done
    - market
        - ticker
    """
    if os.path.isdir(stock_data_root_path):
        list_dir = os.listdir(stock_data_root_path)
        for market in list_dir:
            market_path = os.path.join(stock_data_root_path, market)
            if os.path.isdir(market_path):
                tickers = os.listdir(market_path)
                for ticker in tickers:
                    ticker_path = os.path.join(market_path, ticker)
                    if os.path.isfile(ticker_path):
                        ticker_name = os.path.basename(
                            ticker_path).split('_')[0]
                        df = pd.read_csv(ticker_path)
                        element = sql.get_id()
                        index_ = []
                        data_flag = 0

                        for e in element:
                            for key in df.keys():
                                if key in e:
                                    index_.append(key)
                                    data_flag += 1
                                    break

                        print(element)
                        if data_flag == len(element)-2:
                            df = df[index_]
                            # df = df.where(pd.notnull(df), None)
                            table_ = np.array(df)
                            sql.insert_table(table_, market, ticker_name)
                            market_d_path = os.path.join(done_path, market)
                            os.makedirs(market_d_path, exist_ok=True)
                            ticker_d_path = os.path.join(market_d_path, ticker)
                            # os.makedirs(ticker_d_path,exist_ok=True)
                            shutil.move(ticker_path, ticker_d_path)


def fdrSave(file_path, data, index=False, keys=None):
    if keys:
        data_df = pd.DataFrame(data, columns=keys)
    else:
        data_df = pd.DataFrame(data)
    data_df.to_csv(file_path, index=index)


def arraylist2dict(key_array, arraylist):
    res = dict()
    for i in range(len(arraylist)):
        for j in range(len(key_array)):
            key = key_array[j]
            if not key in res.keys():
                res[key] = [arraylist[i][j]]
            else:
                res[key].append(arraylist[i][j])
    return res


def getMarketName(market, file_path):
    market = str(market)
    dir_path = os.path.dirname(file_path)
    base_path = os.path.basename(file_path)
    last_file = os.path.join(dir_path, market+"_"+base_path)
    return last_file


def exchangeInfoRenewal(from_v, into_v, root_path):
    file_p = from_v.lower()+'2'+into_v.lower()
    cmd_p = from_v.upper()+'/'+into_v.upper()
    exchange_market = getMarketName(file_p, root_path/'exchange.csv')
    if os.path.isfile(exchange_market) is False:
        df = fdr.DataReader(cmd_p, '1900-01-01')
        if len(df.keys()) > 0:
            fdrSave(exchange_market, df, True)
    else:
        df = pd.read_csv(exchange_market)
        keys = list(df.keys())
        dfl = np.array(df)
        last_date = dfl[-1][0]
        df = fdr.DataReader(cmd_p, last_date)
        df_n = np.array(df)
        if len(df_n) > 1:
            for df_i in df_n[1:]:
                dfl.append(df_i)
        fdrSave(exchange_market, dfl, keys=keys)


def stockInfoRenewal(code, root_path, market):
    mkdir = root_path/market
    mkdir.mkdir(exist_ok=True)
    stock_market = getMarketName(code, root_path/market/'stock.csv')
    cmd_p = code
    if os.path.isfile(stock_market) is False:
        df = fdr.DataReader(cmd_p)
        if len(df.keys()) > 0:
            fdrSave(stock_market, df, True)
    else:
        df = pd.read_csv(stock_market)
        keys = list(df.keys())
        if '1' in keys:
            df = fdr.DataReader(cmd_p)
            keys = df.keys()

        dfl = np.array(df)
        last_date = dfl[-1][0]
        df = fdr.DataReader(cmd_p, last_date)
        if 'Date' in df.keys():
            df_n = np.array(df)
            if len(df_n) > 1:
                temp = []
                for df_i in df_n[1:]:
                    temp.append(df_i)
                dfl = arraylist2dict(keys, np.array(temp))
            fdrSave(stock_market, dfl)


def stockInfofind(code, root_path):
    stock_market = getMarketName(code, root_path/'stock_list.csv')
    cmd_p = code
    if os.path.isfile(stock_market) is False:
        df = fdr.StockListing(cmd_p)
        if len(df.keys()) > 0:
            fdrSave(stock_market, df, True)


def getCode(market, root_path, col=1):
    stock_market = getMarketName(market, root_path/'stock_list.csv')
    if os.path.isfile(stock_market):
        df = pd.read_csv(stock_market)
        code = []
        dfn = np.array(df)
        for d in dfn:
            code.append(d[col])
        return code
    else:
        stockInfofind(market, root_path)
        return getCode(market, root_path, col)


class StockTable(DataBase):
    def __init__(self, host,user,pw,db,table_name="stock"):
        super(StockTable, self).__init__(host,user,pw,db)
        self.table_name = table_name
        self.table_query = {
            # "ID": 'int NOT NULL',
            "Market": 'varchar(10) NOT NULL',
            "Ticker": 'varchar(15) NOT NULL',
            "Date": 'Date NOT NULL',
            "Open": 'float',
            "High": 'float',
            "Close": 'float',
            "Volume": 'bigint UNSIGNED',
        }
        self.key =  'PRIMARY KEY (ID, Date), \
                     FOREIGN KEY (ID) REFERENCES stockcode(id)'
    
    def getCodes(self):
        table_name = self.table_name
        cur = self.conn.cursor()
        sql = "SELECT Market, Ticker FROM {} GROUP BY Market, Ticker".format(table_name)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def getLastDate(self,market,ticker):
        table_name = self.table_name
        cur = self.conn.cursor()
        sql = f"SELECT * FROM {table_name} \
            WHERE (Market,Ticker,Date) IN (\
            SELECT Market,Ticker,MAX(Date) \
            FROM {table_name} \
            GROUP BY Market,Ticker \
            );"
        time = self.send_query(sql)[0]['Date']
        time = time+datetime.timedelta(days=1)
        return time.strftime("%Y-%m-%d")

    def insertData(self,market,ticker,data):
        data.reset_index(drop=False,inplace=True)
        ata_df = data
        print(ata_df)
        ata_df['Market'] = market
        ata_df['Ticker'] = ticker

        ata_df = ata_df[list(self.table_query.keys())]
        self.insert_table(np.array(ata_df))


class StockCodeTable(DataBase):
    def __init__(self, host,user,pw,db,table_name="stockcode"):
        super(StockCodeTable, self).__init__(host,user,pw,db)
        self.table_name = table_name
        self.table_query = {
            "Market": 'varchar(10) NOT NULL',
            "Ticker": 'varchar(15) NOT NULL',
            "id":'int(10) NOT NULL AUTO_INCREMENT'
        }
        self.key =  'PRIMARY KEY (id)'

    def getCodes(self):
        table_name = self.table_name
        cur = self.conn.cursor()
        sql = "SELECT Market, Ticker FROM {} GROUP BY Market, Ticker".format(table_name)
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def delData(self):
        sql = f'DELETE FROM {self.table_name}'
        cur = self.conn.cursor()
        cur.execute(sql)

    def insertID(self,dict_table):
        codes = self.getCodes()
        tables = comp_list_w_list(codes,dict_table)
        if len(tables)>0:
            self.insert_table(tables)
    
    def getID(self,market,ticker):
        table_name = self.table_name
        cur = self.conn.cursor()
        sql = f"SELECT id FROM {table_name} WHERE Market={market}, Ticker={ticker}".format(table_name)
        cur.execute(sql)
        result = cur.fetchall()
        return result


    
def getLiveCodes(markets=[
        'KRX', 'KOSPI','KOSDAQ',
        'NYSE','S&P500','NASDAQ',
        'SSE','HKEX','TSE','SZSE','HOSE','AMEX'
    ]):
    codes = []
    if isinstance(markets,list) == False:
        markets = [markets]
    for market in markets:
        code = fdr.StockListing(market)
        if 'Code' in code.keys():
            codes.append([market,code['Code']])
        elif 'Symbol' in code.keys():
            codes.append([market,code['Symbol']])
    return codes

if __name__ == "__main__":
    host = 'db'
    public_db = 'public'
    user_c = os.environ.get('MDASH__database__USER')
    user_p = os.environ.get('MDASH__database__PASSWD') 
    stock = StockTable(host,user_c,user_p,public_db)
    stockcode = StockCodeTable(host,user_c,user_p,public_db)
    codes = stockcode.getCodes()
    l_code = list(getLiveCodes())
    lt_code = []
    for market in l_code:
        m = market[0]
        tickers = market[1]
        for ticker in tickers:
            lt_code.append({'Market':m,'Ticker':ticker})

    for code in lt_code:
        if code in codes:
            l_date = stock.getLastDate(code['Market'],code['Ticker'])
        else:
            l_date = '1900-01-01'
            stockcode.insertID(code)
        last_update_date = datetime.datetime.strptime(l_date,'%Y-%m-%d')
        print(last_update_date)
        now_date = datetime.datetime.now()
        delta_time = now_date - last_update_date
        if delta_time.days > 1:
            ma = code['Market']
            ti = code['Ticker']
            df = fdr.DataReader(code['Ticker'], l_date,datetime.datetime.now().strftime("%Y-%m-%d"))
            stock.insertData(code['Market'],code['Ticker'],df)
            print(f"update: {ma}-{ti}")

        

    """
    현재 시점의 시장별 상장종목 리스트를 가져올 수 있음
    종목코드, 시장, 종목명, 섹터, 산업군, 상장일, 결산월, 대표자, 홈페이지, 사업체 지역을 알 수 있음
    과거 특정 시점의 상장종목 리스트는 알 수 없으나 상장폐지 종목을 조회할 수 있음
    save ${MARKET}_${file_name}.csv
    # 가장 최근 영업일의 시장별 종목리스트를 가져옴
    상장일 기준으로 현재 시간까지의 자료를 가져올 필요가 있음.
    과거의 데이터는 날짜를 기준으로 가져오는 것이 맞겠으나, 내가 실시간으로 수집하는 것은 단순히 현시점으로 쌓아가도 괜찮을듯?
    데이터를 가져오는 방법, 환율을 가져오는 방법을 구현함.
    주가 데이터를 가져오는 것을 구현하기
    """
    # getMarketInfo('KRX',last_file)
    # 한국거래소 상장종목 전체
    # print(stock_info)
    # df_krx = fdr.StockListing('KRX') # 현재 가격관련 정보만 나온다.
    # exchangeInfoRenewal('usd','krw',root_path)
    # exchangeInfoRenewal('usd','hkd',root_path)
    # stockInfoRenewal('005930',root_path)
    # stockInfofind('KRX',root_path)
    root_path = Path("./stock-files")
    root_path.mkdir(exist_ok=True)
    delisting = ['KRX-DELISTING']
    administrative=['KRX-ADMINISTRATIVE']

    futures = ['NG','ZG','ZI','HG']
    bond = ['KR1YT=RR','KR10YT=RR','US1MT=X','US10YT=X']


    def getDeadCodes():
        codes = []
        delisting = ['KRX-DELISTING']
        for market in delisting:
            code = fdr.StockListing(market)
            code_ = list(code.keys())
            print(code_)
            if 'Code' in code.keys():
                codes.append({market:code['Code']})
            elif 'Symbol' in code.keys():
                codes.append({market:code['Symbol']})
        return codes

    def getIndexCodes():
        codes = []
        index = ['NASDAQCOM','HSN1F']
        for market in index:
            code = fdr.StockListing(market)
            code_ = list(code.keys())
            print(code_)
            if 'Code' in code.keys():
                codes.append({market:code['Code']})
            elif 'Symbol' in code.keys():
                codes.append({market:code['Symbol']})
        return codes

    # print((getDeadCodes()))
        # for code in codes:
            # stockInfoRenewal(str(code), root_path, market)
    # df = fdr.DataReader('EUR/KRW', '1900-01-01')
    # df = fdr.DataReader('USD/HKD', '1900-01-01')
    # print(df)

    # # stocks.info()

    # """
    # 2.2. pykrx
    # 특정 시점의 상장 종목코드 조회 가능
    # 해당 종목코드의 종목명을 조회하는 함수가 별도로 존재
    # """
    # # 날짜를 명시해주지 않으면 가장 최근 영업일의 시장별 종목리스트를 가져옴
    # tickers = stock.get_market_ticker_list()
    # # tickers = stock.get_market_ticker_list('2010-01-01')
    # # tickers[:6], tickers[-6:]

    # """
    # 3. 상장종목의 주가 조회
    # 이번에는 상장 종목의 주가 정보를 조회해보자. 주가 정보를 제공하는 패키지들은 보통 OHLCV(시가/고가/저가/종가/거래량) 형태로 데이터를 제공하며,
    # 액면분할 등을 고려한 수정주가를 보여주는데 패키지에 따라 거래량은 보정이 안된 경우가 있다. 이번 글에서는 삼성전자(005930)의 주가 데이터 조회를 예시로 들어보려고 한다.
    # 삼성전자의 상장일은 1975년 6월 11일인데 이 시점부터 데이터를 제공하는 패키지는 없었고, 패키지마다 데이터 제공 시작시점이 모두 달랐다.

    # 3.1. FinanceDataReader
    # 조회 시점에 따라 조회할 수 있는 최대 과거 시점이 변동됨
    # 예를 들어, 2022-03-22에 조회했을 때는 1998-02-05부터 조회됐었는데, 2022-03-23에 조회했을 때는
    # 1998-02-06부터 조회됨 - 네이버금융에서 데이터를 가져오는데 일자가 지날 때 마다 과거 데이터를 삭제하는 것으로 보임
    # 액면분할을 반영한 수정주가가 조회되는데 거래량은 보정되지 않은 상태임
    # """
    # start_date = '1975-06-11'
    # end_date = '2022-03-23'

    # stock_code = '005930'
    # df_fdr = fdr.DataReader(stock_code, start=start_date, end=end_date)

    # """
    # 3.2. pykrx
    # 1990년 데이터부터 조회 가능
    # 수정주가가 디폴트로 조회됨(adjusted 옵션으로 수정주가 여부 설정가능)
    # adjusted=False로 조회하면 1995-05-02부터 조회되고, 거래대금과 등락률 칼럼이 추가됨
    # 액면분할을 반영한 수정주가가 조회되는데 거래량은 보정되지 않은 상태임
    # """
    # df_pykrx = stock.get_market_ohlcv_by_date(fromdate=start_date,
    #                                           todate=end_date,
    #                                           ticker="005930", adjusted=False)
    # """
    # 3.3. pandas_datareader
    # 데이터소스를 naver로 지정하면 1990년 데이터부터 조회할 수 있고, yahoo로 지정하면 2000년 데이터부터 조회할 수 있음
    # 액면분할이 고려된 수정주가로 조회됨
    # yahoo finance를 데이터소스로 사용할 때는 종목코드 뒤에 코스피 종목인 경우 .KS, 코스닥 종목인 경우 .KQ를 붙여줘야 함
    # ex) 005930.KS
    # , exchange='KRX-DELISTING'
    # """

    # """
    # 3.4. yfinance
    # yahoo finance를 데이터 소스로 사용하는 패키지이기 때문에 위에서 설명한 바와 같이 코스피 종목에는 .KS, 코스닥 종목에는 .KQ를 붙여줘야 함
    # 가장 다양한 정보 확인 가능 - 배당정보, 분할정보, 재무정보 등
    # 2000년 데이터부터 조회 가능
    # end에 설정한 일자의 전일자까지 조회되기 때문에 조회하고자 하는 종료일+1일을 end에 넣어줘야함
    # 분단위 데이터도 조회 가능하지만 조회 가능한 기간에 제한이 있음
    # """
    # ticker = yf.Ticker('005930.KS')

    # ticker.history(
    #     interval='1d',  # 1m, etc
    #     start=start_date,
    #     end='2022-03-24',
    #     actions=True,
    #     auto_adjust=True)

    # # 재무정보도 조회가능
    # # ticker.financials

    # """
    # 4. 상장폐지 종목의 주가 조회
    # 상장폐지 종목의 주가 조회는 FinanceDataReader, pykrx, pandas_datareader에서 데이터 소스를 naver로 설정했을 때만 가능하다.
    # yahoo finance에서는 상장폐지 종목에 대한 정보를 제공하지 않고 있는 것 같다. 상장폐지 종목의 리스트는 앞에서 설명한 것처럼 FinanceDataReader를 통해 조회하면 된다.
    # KRX delisting stock data 상장폐지된 종목 가격 데이터 (상장일~상장폐지일)
    # krx_delisting[krx_delisting.Symbol == '001047']
    # """
    # """
    # krx나 naver를 데이터 소스로 사용하는 경우에는 거래량이 액면분할을 고려하지 않은 상태로 조회되고,
    # yahoo finance를 데이터 소스로 사용하는 경우에는 거래량이 액면분할을 고려한 상태로 조회된다(1483967*50=74198350).
    # """

    # tsla_df = yf.download('TSLA',
    #                       start='2019-01-01',
    #                       end='2019-12-31',
    #                       progress=False)
    # tsla_df.head()

    # tsla_df = yf.download('TSLA')

    # ticker = yf.Ticker('TSLA')

    # tsla_df = ticker.history(period="max")

    # tsla_df['Close'].plot(title="TSLA's stock price")

    # yahoo_financials = YahooFinancials('TSLA')

    # data = yahoo_financials.get_historical_price_data(start_date='2000-01-01',
    #                                                   end_date='2019-12-31',
    #                                                   time_interval='weekly')

    # tsla_df = pd.DataFrame(data['TSLA']['prices'])
    # tsla_df = tsla_df.drop('date', axis=1).set_index('formatted_date')
    # tsla_df.head()
    # assets = ['TSLA', 'MSFT', 'FB']

    # yahoo_financials = YahooFinancials(assets)

    # data = yahoo_financials.get_historical_price_data(start_date='2019-01-01',
    #                                                   end_date='2019-12-31',
    #                                                   time_interval='weekly')

    # prices_df = pd.DataFrame({
    #     a: {x['formatted_date']: x['adjclose'] for x in data[a]['prices']} for a in assets
    # })
