import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wifi"
    )
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version", db_info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database:", record[0])
except mysql.connector.Error as e:
    print("Error connecting to MySQL", e)
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")