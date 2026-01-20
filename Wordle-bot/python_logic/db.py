import pyodbc
import os
import csv

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=LIAM\\SQLEXPRESS;"
    "Database=Dictionary;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

def get_all_words():
    if os.path.exists('words.csv'):
        words = []
        with open('words.csv', 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row:
                    words.append(row[0])      
        return words
    else:
        cursor.execute("SELECT word FROM words WHERE LEN(word) = 5;")
        rows = [row[0] for row in cursor.fetchall()]
        with open('words.csv', 'w', encoding='utf-8') as f:
            csv.writer(f).writerows([[word] for word in rows])
        return rows

def get_all_wordle_answers():
    cursor.execute("SELECT words FROM wordle;")
    return [row[0] for row in cursor.fetchall()]

def close_connection():
    conn.close()