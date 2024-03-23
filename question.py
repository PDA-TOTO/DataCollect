import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWARD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

df = pd.read_excel('./question.xlsx')
print(df)

engine = create_engine(f'mysql+pymysql://{USER}:{PASSWARD}@{HOST}:{PORT}/{DATABASE}')

df.to_sql(name='QUIZ', con=engine, if_exists='replace', index=False)
