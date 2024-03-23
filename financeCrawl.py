
import os
import requests
from dotenv import load_dotenv
import ast
from pykrx import stock
from pykrx import bond
import mysql.connector
import time
# import mysql

load_dotenv()
APPKEY = os.getenv("APPKEY")
APPSECRET = os.getenv("APPSECRET")
AUTH = os.getenv("AUTH")

from mysqlconnect import connet_to_mysql

connection = connet_to_mysql()

cursor = connection.cursor()


fid_cond_mrkt_div_code = "J"
fid_div_cls_code = "1"
custtype = "P"

def get_finance_data(code):
    """
    예시 {'code': '005930', 'yymm': '201609', 'rev': '1485350.00', 'income': '200199.00', 'netIncome': '156381.00'}
    """

    # fid_input_iscd ="005930"
    fid_input_iscd =code
    params = {
        'fid_cond_mrkt_div_code': 'J',
        'fid_input_iscd': code,
        'fid_div_cls_code' : '1'
    }
    headers = {
        "content-type" : "application/json; charset=utf-8",
        "authorization" : AUTH,
        "appkey" : APPKEY,
        "appsecret" : APPSECRET,
        "tr_id" : "FHKST66430200",
        "custtype" : custtype
    }
    
    response = requests.get(f'https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/finance/income-statement',params=params,headers=headers)
    list  = ast.literal_eval(response.text)

    feteched_data = list['output']
    for elem in feteched_data:
        yymm ,rev, income, netIncome = elem['stac_yymm'], int(float(elem['sale_account'])), int(float(elem['bsop_prti'])), int(float(elem['thtr_ntin']))
        print(yymm ,rev , income, netIncome)
        query = f"INSERT INTO FINANCE (code, yymm, rev, income, netIncome) VALUES ('{code}', '{yymm[:4]+'.'+yymm[4:]}', {rev}, {income}, {netIncome})"
        cursor.execute(query)
        print({"code" : fid_input_iscd, "quarter" : yymm, "rev" : rev, "income" : income, "netIncome":netIncome})

# 예시- {'code': '005930', 'yymm': '201609', 'roe_val': '11.94', 'eps': '1881.00', 'bps': '22708.00', 'lblt_rate': '36.17'}        
def get_jaemu_data(code): #재무라는 뜻
    """
    {'code': '005930', 'yymm': '201609', 'roe_val': '11.94', 'eps': '1881.00', 'bps': '22708.00', 'lblt_rate': '36.17'} 
    """
    # fid_input_iscd ="005930"
    fid_input_iscd =code
    headers = {
        "content-type" : "application/json; charset=utf-8",
        "authorization" : AUTH,
        "appkey" : APPKEY,
        "appsecret" : APPSECRET,
        "tr_id" : "FHKST66430300",
        "custtype" : custtype
    }
    
    params = {
        'fid_cond_mrkt_div_code': 'J',
        'fid_input_iscd': code,
        'fid_div_cls_code' : '1'
    }

    print(params,headers)
    response = requests.get(f'https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/finance/financial-ratio',params=params,headers=headers)
    list  = ast.literal_eval(response.text)
    feteched_data = list['output']
    for elem in feteched_data:
        yymm ,roe_val, eps, bps,lblt_rate = \
        elem['stac_yymm'], elem['roe_val'], float(elem['eps']), float(elem['bps']), float(elem['lblt_rate'])
        query = f"INSERT INTO JAEMU (code, yymm, roe_val, eps, bps, lblt_rate ) VALUES ('{code}', '{yymm[:4]+'.'+yymm[4:]}' , {roe_val}, {eps}, {bps},{lblt_rate})"
        cursor.execute(query)
        print({"code" : fid_input_iscd, "yymm" : yymm,"roe_val" : roe_val, "eps" : eps, "bps" : bps, "lblt_rate": lblt_rate})
        
        
# get_finance_data("005930")
# get_jaemu_data("005930")

tickers = stock.get_market_ticker_list("20240315")
for elem in tickers:
    print(elem)
    # get_finance_data(elem)
    get_jaemu_data(elem)
    time.sleep(1)
    connection.commit()

# connection.commit()
cursor.close()
connection.close()
# print(len(tickers))
