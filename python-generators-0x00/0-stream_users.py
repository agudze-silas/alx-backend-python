import mysql.connector
from mysql.connector import Error
from itertools import islice


def stream_users():
    """
    Generator that fetches rows from user_data table one by one.
    """
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Silas@020",   # <-- replace with your MySQL password
            database="ALX_prodev"
        )
    try:
        cursor = connection.cursor(dictionary=True) 
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            yield row   

    except Error as e:
        print(f"❌ Error fetching data: {e}")
    finally:
        cursor.close()

def main():
        
    for user in islice(stream_users(), 6):
        print(user)
       


if __name__ == "__main__":
    main()