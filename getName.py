from pykrx import stock
from pykrx import bond
import mysql.connector
from mysqlconnect import connet_to_mysql

connection = connet_to_mysql()
cursor = connection.cursor()


# 주식 종목이름 가져오는 함수
# for ticker in stock.get_market_ticker_list():
#     print({"code" : ticker, "name" : stock.get_market_ticker_name(ticker)})    
#     query = f"INSERT INTO CODE (krxCode, name, type) VALUES ('{ticker}', '{stock.get_market_ticker_name(ticker)}', 'STOCK')"
#     cursor.execute(query)
#     connection.commit()

#ETF 종목이름 가져오는 함수
for ticker in stock.get_etf_ticker_list():
    print({"code" : ticker, "name" : stock.get_etf_ticker_name(ticker)})
    query = f"INSERT INTO CODE (krxCode, name, type) VALUES ('{ticker}', '{stock.get_etf_ticker_name(ticker)}',('ETF'))"
    cursor.execute(query)
    connection.commit()

cursor.close()
connection.close()