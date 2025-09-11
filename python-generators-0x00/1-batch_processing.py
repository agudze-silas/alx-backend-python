import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Yields one batch (list of rows) at a time.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",           
            password="Silas@020",   
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch   

    except Error as e:
        print(f" Error streaming data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users, filtering only those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):     
        filtered = [user for user in batch if int(user["age"]) > 25]  
        yield filtered  


if __name__ == "__main__":
    for filtered_batch in batch_processing(batch_size=25): 
        for user in filtered_batch:
            print(user)
