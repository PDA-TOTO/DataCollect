from pykrx import stock
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
from mysqlconnect import connet_to_mysql
import json

#네이버 내에 와이즈 리포트(주식)
def crawl_beta(code) : 
    driver = webdriver.Chrome()
    driver.get(f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}')
    html2 = driver.page_source
    soup = BeautifulSoup(html2, 'html.parser')
    script_tag = soup.select(".body table tbody tr td")
    beta = script_tag[5].get_text().strip()
    return beta

#네이버 내에 와이즈 리포트(ETF)
def crawl_beta2(code) : 
    driver = webdriver.Chrome()

    driver.get(f'https://navercomp.wisereport.co.kr/v2/ETF/Index.aspx?cn=&cmp_cd={code}&menuType=block')
    html2 = driver.page_source
    soup = BeautifulSoup(html2, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        script_text = script_tag.get_text()
        if 'var status_data' in script_text:
            json_data = script_text.split('var status_data = ')[1].split(';')[0]
            status_data = json.loads(json_data)
            beta = status_data.get('YR_BETA')
    return beta

    # # url = f'https://navercomp.wisereport.co.kr/v2/ETF/Index.aspx?cn=&cmp_cd={code}&menuType=block'
    # html2 = driver.page_source
    # soup = BeautifulSoup(html2, 'html.parser')
    # # print(soup)
    # script_tag = soup.select('script[type="text/javascript"]')
    # script_text = script_tag.get_text()
    # print(script_text)
    # status_data = json.loads(script_text.split('=', 1)[1].strip().rstrip(';'))

    # # YR_BETA 값을 출력합니다.
    # print("YR_BETA:", status_data['YR_BETA'])
    # # beta = script_tag[5].get_text().strip()
    # return beta

#
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
    
# etf_crawl("102780")
# stock_crawl('005930')

# stocks = stock.get_market_ticker_list("20240315")
# etfs = stock.get_etf_ticker_list("20240315")

connection = connet_to_mysql()
cursor = connection.cursor()

# for code in etfs:
#     print(code)
#     query = f"INSERT INTO FINANCE3 (code) VALUES ('{code}')"
#     try :
#         cursor.execute(query)
#         connection.commit()
#         print(query)
#     except Exception as e:
#         print(e)

query = "select code from FINANCE3 where beta is null"
cursor.execute(query)
result = cursor.fetchall()

# print(result)
# print(crawl_beta2("476690"))
# print(crawl_beta2("476690"))

for elem in result:
    print(elem[0])
    try :
        beta = crawl_beta2(elem[0])
        # beta = etf_crawl(elem[0])
        query = f"update FINANCE3 set beta = {beta} where code = '{elem[0]}'"
        cursor.execute(query)
        connection.commit()
        print(query)
    except Exception as e:
        print("에러발생 수고")
     
# for code in stock.get_etf_ticker_list("20240225") :
#     print(code)
#     try :
#         try : 
#             beta = stock_crawl(code)
#         except :
#             beta = etf_crawl(code) 

#         query = f"INSERT INTO FINANCE3 (code, beta) VALUES ('{code}', '{beta}')"
#         cursor.execute(query)
#         connection.commit()
#         print(query)    
#     except Exception as e:
#         print("fail")    

cursor.close()
connection.close()