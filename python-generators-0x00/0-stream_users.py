import mysql.connector
from mysql.connector import Error


def fetch_users_generator(connection):
    """
    Generator that fetches rows from user_data table one by one.
    """
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
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Silas@020",   # <-- replace with your MySQL password
            database="ALX_prodev"
        )

        # Use the generator to fetch users
        for user in fetch_users_generator(connection):
            print(user)

        connection.close()


if __name__ == "__main__":
    main()