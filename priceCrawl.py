import pandas as pd
import os
import requests
# from dotenv import load_dotenv
import ast
from pykrx import stock
from pykrx import bond
import mysql.connector
from mysqlconnect import connet_to_mysql

connection = connet_to_mysql()

cursor = connection.cursor()

#주식의 시,고,저,종 code명 가져오는 함수
for code in stock.get_market_ticker_list("20240315")[737:]:
    df = stock.get_market_ohlcv("20190101", "20240315", code)
    df['code']= code
    df_reset = df.reset_index()
    df_reset=df_reset[['날짜','시가','고가','저가','종가','code']]
    for idx, row in df_reset.iterrows():
        row_dict = {column: row[column] for column in df_reset.columns}
        insert_date , insert_sPr, inser_hPr, insert_iPr, insert_ePr, insert_code \
            = row_dict['날짜'], row_dict['시가'],row_dict['고가'],row_dict['저가'],row_dict['종가'],row_dict['code']
        query = f"INSERT INTO PRICE (date, sPr, hPr, iPr, ePr, code) VALUES ('{insert_date}', '{insert_sPr}', {inser_hPr}, {insert_iPr}, {insert_ePr}, '{code}')"
        cursor.execute(query)
    connection.commit()
    
#ETF의 시,고,저,종 code명 가져오는 함수   
for code in stock.get_etf_ticker_list("20240315"):
    df = stock.get_market_ohlcv("20190101", "20240315", code)
    df['code']= code
    df_reset = df.reset_index()[['날짜','시가','고가','저가','종가','code']]
    for idx, row in df_reset.iterrows():
        row_dict = {column: row[column] for column in df_reset.columns}
        insert_date , insert_sPr, inser_hPr, insert_iPr, insert_ePr, insert_code \
            = row_dict['날짜'], row_dict['시가'],row_dict['고가'],row_dict['저가'],row_dict['종가'],row_dict['code']
        query = f"INSERT INTO PRICE (date, sPr, hPr, iPr, ePr, code) VALUES ('{insert_date}', '{insert_sPr}', {inser_hPr}, {insert_iPr}, {insert_ePr}, '{code}')"
        cursor.execute(query)
    connection.commit()
    print(f"{code} completed")

cursor.close()
connection.close()