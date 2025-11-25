import json
import os
from mysql.connector import connect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

#load valid json file
input_file = './data/task1_d_valid.json'

with open(input_file,'r',encoding='utf-8') as f:
    data = json.load(f)

# Connect to mysql
conn = connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

cursor = conn.cursor()

# Create Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS book_raw(
        id INT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        genre VARCHAR(100),
        publisher VARCHAR(100),
        year INT,
        price DECIMAL(10,2)
    )
'''
)

# Data insertion
insert_query = 