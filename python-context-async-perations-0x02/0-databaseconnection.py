import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open connection and return cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if no exception, rollback otherwise
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
            print(f"Error: {exc_val}")
        # Close connection
        self.connection.close()
        return False  # re-raise exception if any


# Example usage
if __name__ == "__main__":
    # Assuming there is a "users" table in test.db
    with DatabaseConnection("test.db") as cursor:
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        for row in results:
            print(row)
