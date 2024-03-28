
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWARD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

def connet_to_mysql():
    # print(HOST,PORT,USER,PASSWARD,DATABASE)
    connection = mysql.connector.connect(
        # host= 'localhost',
        # port="3312",
        # user='root',
        # password='root',
        # database='my_database'
        host= HOST,
        port=PORT,
        user=USER,
        password=PASSWARD,
        database=DATABASE
    )
    print("connect")
    return connection
