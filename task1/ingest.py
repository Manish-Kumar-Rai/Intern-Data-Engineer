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
    CREATE TABLE IF NOT EXISTS books_raw(
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_id VARCHAR(50),
        title VARCHAR(100),
        author VARCHAR(100),
        genre VARCHAR(100),
        publisher VARCHAR(100),
        year INT,
        price DECIMAL(10,2)
    )
'''
)

# Data insertion
insert_query = '''
    INSERT INTO books_raw (book_id,title,author,genre,publisher,year,price)
    VAlUES (%s,%s,%s,%s,%s,%s,%s)
'''

for book in data:
    cursor.execute(insert_query,(
        str(book.get('id')),
        book.get('title'),
        book.get('author'),
        book.get('genre'),
        book.get('publisher'),
        int(book.get('year')),
        float(book.get('price'))
    ))

conn.commit()
print('Data ingested successfully.')

cursor.close()
conn.close()