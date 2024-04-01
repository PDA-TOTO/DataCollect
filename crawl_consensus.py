from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
from mysqlconnect import connet_to_mysql
import json
from pykrx import stock
from pykrx import bond

connection = connet_to_mysql()
cursor = connection.cursor()

def crawl_consensus(code) : 
    url = f'https://m.stock.naver.com/api/stock/{code}/integration'
    res = requests.get(url)   
    
    parsed = json.loads(res.text)
    return parsed['consensusInfo']['priceTargetMean']

# for ticker in stock.get_market_ticker_list():
#     try :
#         consen = int(crawl_consensus(ticker).replace(",",""))
#         query = f"UPDATE FINANCE SET consensus = {consen} WHERE code = {ticker}"
#         cursor.execute(query)
#         connection.commit()
#         print("commit 성공")
#     except Exception as e:
#         print(e)
#         print("이거 없는거임 수공")


def crawl_pbr(code) : 
    url = f'https://m.stock.naver.com/api/stock/{code}/integration'
    res = requests.get(url)   
    
    parsed = json.loads(res.text)
    print(parsed['totalInfos'][14]["value"][:-1])
    return parsed['totalInfos'][14]["value"][:-1]
# crawl_pbr("006840")

for ticker in stock.get_market_ticker_list():
    try :
        pbr = float(crawl_pbr(ticker))
        query = f"UPDATE FINANCE SET pbr = {pbr} WHERE code = {ticker}"
        cursor.execute(query)
        connection.commit()
        print("commit 성공")
    except Exception as e:
        print(e)
        print("이거 없는거임 수공")


# cursor.close()
# connection.close()