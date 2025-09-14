import sqlite3

class ExecuteQuery:
    """
    A reusable context manager that handles database connection and query execution.
    Takes a query and parameters as input and returns the query results.
    """
    
    def __init__(self, db_path, query, parameters=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            db_path (str): Path to the database file
            query (str): SQL query to execute
            parameters (tuple/list, optional): Parameters for the query
        """
        self.db_path = db_path
        self.query = query
        self.parameters = parameters or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager - establish connection and execute query.
        
        Returns:
            list: Results from the executed query
        """
        print(f"Opening database connection to: {self.db_path}")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        print(f"Executing query: {self.query}")
        if self.parameters:
            print(f"With parameters: {self.parameters}")
        
        # Execute the query
        if self.parameters:
            self.cursor.execute(self.query, self.parameters)
        else:
            self.cursor.execute(self.query)
        
        # Fetch all results
        self.results = self.cursor.fetchall()
        print(f"Query executed successfully. {len(self.results)} rows returned.")
        
        return self.results
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - clean up database connection.
        
        Args:
            exc_type: Exception type (if any)
            exc_value: Exception value (if any)
            traceback: Exception traceback (if any)
        """
        if self.cursor:
            self.cursor.close()
            print("Database cursor closed")
        
        if self.connection:
            if exc_type is not None:
                # Rollback if there was an exception
                self.connection.rollback()
                print("Transaction rolled back due to exception")
            else:
                # Commit if no exceptions occurred
                self.connection.commit()
                print("Transaction committed successfully")
            
            self.connection.close()
            print("Database connection closed")
        
        # Return False to propagate any exceptions
        return False
