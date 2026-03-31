import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="crypto_portfolio_db"
    )
    return connection