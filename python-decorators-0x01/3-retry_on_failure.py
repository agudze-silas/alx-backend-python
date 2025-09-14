import time
import sqlite3 
import functools

# --- Decorator: opens and closes DB connection ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# --- Decorator: retries function on failure ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[RETRY] Attempt {attempt}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[ERROR] Attempt {attempt} failed: {e}")
                    last_exception = e
                    time.sleep(delay)
            print("[RETRY] All attempts failed.")
            raise last_exception
        return wrapper
    return decorator

# --- Decorators in the correct order ---
@retry_on_failure(retries=3, delay=1)
@with_db_connection
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Attempt to fetch users with retry logic ---
users = fetch_users_with_retry()
print(users)
