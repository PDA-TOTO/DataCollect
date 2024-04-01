import requests
import json
from mysqlconnect import connet_to_mysql
from pykrx import stock

#네이버에서 개요 크롤링 하는 파일

connection = connet_to_mysql()

cursor = connection.cursor()

def crawl_gaeyo(code):
    url = f'https://m.stock.naver.com/api/stock/{code}/finance/annual'
    result = requests.get(url)
    data = result.text
    parsed = json.loads(data)
    return parsed['corporationSummary']
    # print(parsed['corporationSummary'][''])


stocks = stock.get_market_ticker_list("20240301",  market="KOSDAQ")
print(stocks)

for stock in stocks:
    try : 
        result = crawl_gaeyo(stock)
        for key, value in result.items():
            query =f"INSERT into INFO (krxCode, INFO) values ({stock}, '{value}')"
            cursor.execute(query)
            connection.commit()
            print(query)
    except Exception as e:
        print(e)

cursor.close()
connection.close()