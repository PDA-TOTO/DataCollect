import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from openai import OpenAI
from dotenv import load_dotenv
import os 


load_dotenv()

URL= os.getenv("URL")
GPT_KEY = os.getenv("GPT_KEY")


# MYSQL 연결
conn = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="root",
    database="toto-local"
)

cursor = conn.cursor()

# 크롤링
for page in range(1,84):
    params = {'page': page }
    urlResponse = requests.get(url=URL,params=params)
    urlHtml = BeautifulSoup(urlResponse.text, 'html.parser')

    h3List = urlHtml.findAll("h3",{"class":"news-tit"})

    for h3 in h3List:
        href = h3.a["href"]
        articleResponse = requests.get(href)
        articleHtml = BeautifulSoup(articleResponse.text, 'html.parser')

        articleBody= articleHtml.find("div",{"class":"article-body"})

        strong = articleBody.findAll('strong')
        text = articleBody.text.strip()

        answers = [] # 정답 리스트
        questions = [] # 질문 리스트

        for question in strong:
            text = text.replace(question.text,"")

            if '정답' in question.text:

                for answer in question.text:
                    if answer == '①': answers.append(1)
                    elif answer == '②': answers.append(2)
                    elif answer == '③': answers.append(3)
                    elif answer == '④': answers.append(4)

            else:
                questions.append(question.text[2:])

        options = re.split(r'①|②|③|④', text)[1:]

        data = []
        if len(questions)*4 == len(answers)*4 == len(options) :
            for i in range(len(questions)):
                
                # OpenAI API 사용
                client = OpenAI(api_key=GPT_KEY)

                model = "gpt-3.5-turbo"
                messages = [
                        {
                            "role": "system", 
                            "content": "You are responsible for classifying the difficulty level of stock questions."
                        },
                        {
                            "role": "assistant", 
                            "content": """
                                The levels of those questions must be the standard to classify the difficulty level of stock questions.
                                The format of response should be a number like (0, 1, 2 or 3).
                                The questions have been classified as follows: 
                                    Questions:  
                                    '기업가치가 '100억 달러'를 넘어선 것으로 평가받은 비상장 회사를 가리키는 말은?'
                                    '아마존, 네이버 등의 사례처럼 정보기술(IT) 사업으로 출발한 기업이 주도하는 혁신적인 금융 서비스를 가리키는 말은?'
                                    '기업 회의, 인센티브 관광, 국제 회의, 전시회를 뜻한다. 수익성이 뛰어난 신산업으로 평가받고 있는 이 산업은?'
                                    '국가가 저임금 근로자의 삶의 질을 보장하기 위한 목적으로 설정한 임금의 하한선은?'
                                    '재화나 서비스를 한 단위 더 생산하는 데 들어가는 추가 비용을 가리키는 경제학 용어는?'
                                    '최근 미국 연방수사국(FBI)이 해커가 취득한 ‘이것’을 회수하는 데 성공했다. 나카모토 사토시라는 익명의 개발자가 만든 암호화폐인 이것은?'
                                    '특정 상품을 미래의 특정 시기에 시장 가격에 관계없이 미리 정해둔 가격에 팔 수 있는 권리를 뜻하는 말은?'
                                    '기업이 보유한 건물, 기계 등은 시간이 지날수록 경제적 가치가 떨어진다. 회계 처리할 때 이런 가치 감소분을 평가하는 데 쓰는 것은?'
                                    '명품 브랜드가 가격을 대폭 인상했는데도 판매량은 오히려 증가하는 현상을 가장 잘 설명하는 용어는?'
                                    '최근 주요 7개국(G7) 재무장관들이 이 세금을 최저 15%로 설정하는 방안에 합의했다. 기업이 부담하는 세금인 이것은?'    
                                    0

                                    Question:  
                                    '올해 들어 한국의 ‘이것’ 적자가 100억달러를 돌파했다. 일정 기간 한 나라의 총수입과 총수출 간 차이인 이것은?'
                                    '최근 인수합병(M&A) 매물로 나와 전자상거래 업계의 주목을 받은 업체다. G마켓과 옥션을 운영하는 이 회사는?'
                                    '기업이 일반 투자자들에게 재무 내용을 공시하고 주식을 공개하는 절차다. 증시 상장을 가리키는 이 단어는?'
                                    '도로, 항만, 공항, 철도 등의 '사회간접자본'을 뜻하는 약어는?'
                                    '주식, 채권, 원자재, 통화 등을 기초자산으로 하는 특정 지수의 움직임에 따라 수익을 얻을 수 있는 상장지수펀드는?'
                                    '태양광, 풍력 등 재생에너지 발전에 활용되며 여유 전력을 필요할 때 꺼내 쓸 수 있도록 만든 에너지저장장치는?'
                                    '국가가 보유한 자본, 노동 등의 생산요소를 최대한 사용하면서 물가 상승을 유발하지 않고 달성할 수 있는 성장률은?'
                                    '기업에 필요한 기술과 아이디어를 얻기 위해 다른 기업이나 연구조직과 유기적인 협력 관계를 구축하는 ‘개방형 혁신’ 전략은?'
                                    '자신의 필요에 따라 자발적으로 단기 비정규직이나 프리랜서로 일하는 사람들이 늘어나는 경제현상은?'
                                    '스타벅스가 한국에서 햅쌀이나 오미자 음료를, 맥도날드가 인도에서 소고기를 뺀 햄버거를 내놓는 등의 전략에 적합한 표현은?'
                                    1

                                    Question: 
                                    '다음 중 경제 상황과 전망에 대한 소비자들의 인식을 파악할 수 있는 지표는?'
                                    '소비 증가에 따른 기업의 매출 증대, 신년 주가 상승에 대한 기대감 등을 바탕으로 연말에 주가가 오르는 현상은?'
                                    '오늘 코스닥시장에서 A 기업의 주가는 1만원으로 마감했다. 내일 이 기업이 상한가를 기록한다면 주가는 얼마가 될까?'
                                    '다음 중 경우에 따라 마이너스(-) 값으로 떨어지는 것이 가능한 지표는?'
                                    '실업률과 물가상승률은 반비례한다는 주장을 뒷받침할 수 있는 그래프는?'
                                    '금, 달러, 미국 국채의 공통점으로 가장 가까운 것은?'
                                    '불필요한 서비스와 운영비를 최소화해 기존 대형 항공사보다 저렴한 운임을 선보이는 ‘저비용 항공사’를 뜻하는 말은?'
                                    '대출을 받으려는 사람의 소득 대비 전체 금융부채의 원리금 상환액 비율을 말한다. ‘총부채원리금상환비율’을 가리키는 약어는?'
                                    '다음 중 기업이 자금 조달 수단으로 활용할 수 있는 방법이 아닌 것은?'
                                    '증기발생기, 냉각재 펌프, 가압기 등 주요 기기를 하나의 용기에 일체화한 ‘소형모듈원자로’다. 차세대 원전 기술로 주목받는 이것은?'
                                    2

                                    Question: 
                                    '기업가치가 채권을 발행한 국가의 ‘부도 위험’이 높아질 때 함께 상승하는 수치는?'
                                    '미국 중앙은행(Fed)의 연방준비제도이사회가 개최하는 경제정책회의 ‘연방공개시장위원회’를 가리키는 말은?'
                                    '수출 물류와 관련한 기사에서 자주 볼 수 있는 단위다. 20피트(609.6㎝) 표준 컨테이너 1개가 한 단위인 이것은?'
                                    '한 해 증시를 마감하는 연말을 전후로 주가가 오르는 현상을 가리키는 말은?'
                                    '기업 파산, 국가 부도 등의 위험을 사고팔 수 있는 파생금융상품이다. '신용부도스와프'인 이것은?'
                                    '투자자의 은퇴 시기를 목표 시점으로 잡고 생애주기에 따라 포트폴리오를 조정하는 자산배분 펀드는?'
                                    '기업의 외부감사인을 정기적으로 교체해 기업과 감사인 간의 교착관계를 끊고 부실감사를 막겠다는 취지를 내세운 제도는?'
                                    '다음 중 해운산업의 업황을 파악할 수 있는 지수는?'
                                    '국제통화기금(IMF)이 만든 '특별인출권'을 가리킨다. 회원국이 보유하면 외환보유액으로 인정되는 이것은?'
                                    '다음 중 '행동주의 헤지펀드'에 해당하는 곳은?'
                                    3
                                """
                        },
                        {
                            "role": "user", 
                            "content": questions[i]
                        },
                    ]

                response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0,
                    )

                level = response.choices[0].message.content


                if '0' <= level <= '3' :
                    q = (questions[i], answers[i], options[i * 4], options[i * 4 + 1], options[i * 4 + 2], options[i * 4 + 3], int(level))
                    print(q)
                    data.append(q)

            # DB 저장
            sql = "INSERT INTO quiz (question, answer, option1, option2, option3, option4, level) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data)
            
            conn.commit()

cursor.close()
conn.close()
