from pykrx import stock
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re

from mysqlconnect import connet_to_mysql

def crawl_beta(code) : 
    driver = webdriver.Chrome()
    driver.get(f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}')
    html2 = driver.page_source
    soup = BeautifulSoup(html2, 'html.parser')
    script_tag = soup.select(".body table tbody tr td")
    beta = script_tag[5].get_text().strip()
    return beta

def etf_crawl(code):
    url = f'https://comp.fnguide.com/svo2/asp/etf_analysis.asp?pGB=1&gicode=A{code}'
    res = requests.get(url)    
    soup = BeautifulSoup(res.text, "lxml")
    script_tags = soup.find_all('script')
    result = []
    
    for script in script_tags:
        script_content = script.text

        variables = re.findall(r'var\s+(\w+)\s*=\s*(.*?);', script_content, re.DOTALL)

        if variables : 
            result = variables
    
    text = result[17][1].strip().replace('\r\n', '').replace(' ', '')
    beta_value = re.search(r'"val01":"베타","val02":"([^"]+)"', text)
    return beta_value.group(1)

def stock_crawl(code):
    url = f'https://comp.fnguide.com/svo2/asp/SVD_Main.asp?pGB=1&gicode=A{code}'
    res = requests.get(url)    
    # print(res.text)
    soup = BeautifulSoup(res.text, "lxml")
    # print(soup)
    data = soup.find('div',class_='um_table').find_all('td')
    beta = data[7].text
    
    return beta
    



# print(etf_crawl("102780"))
# print(stock_crawl('005930'))

# print(stock_crawl('001465'))

connection = connet_to_mysql()
cursor = connection.cursor()

for code in stock.get_etf_ticker_list("20240225") :
    print(code)
    try :
        try : 
            beta = stock_crawl(code)
        except :
            beta = etf_crawl(code) 

        query = f"INSERT INTO FINANCE3 (code, beta) VALUES ('{code}', '{beta}')"
        cursor.execute(query)
        connection.commit()
        print(query)    
    except Exception as e:
        print("fail")    

# print(stock.get_market_ticker_list("20240225"))

cursor.close()
connection.close()