#!/usr/bin/env python
# coding: utf-8

import mysql.connector
from mysql.connector import Error
import csv
import uuid

# -------------------------------
# Connect to MySQL Server
# -------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Silas@020"
        )
        if connection.is_connected():
            print("✅ Connected to MySQL Server")
            return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

# -------------------------------
# Create database if not exists
# -------------------------------
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database ALX_prodev ensured")
    except Error as e:
        print(f"❌ Error creating database: {e}")

# -------------------------------
# Connect specifically to ALX_prodev
# -------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Silas@020",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("✅ Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"❌ Error while connecting to ALX_prodev: {e}")
        return None

# -------------------------------
# Create user_data table
# -------------------------------
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("✅ Table user_data ensured")
    except Error as e:
        print(f"❌ Error creating table: {e}")

# -------------------------------
# Insert data if not exists
# -------------------------------
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (data["email"],))
        if cursor.fetchone()[0] > 0:
            print(f"⚠️ Skipping duplicate email: {data['email']}")
            return
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, (str(uuid.uuid4()), data["name"], data["email"], data["age"]))
        connection.commit()
        print(f"✅ Inserted {data['name']}")
    except Error as e:
        print(f"❌ Error inserting data: {e}")

# -------------------------------
# Main Seeder Function
# -------------------------------
def main():
    server_conn = connect_db()
    if not server_conn:
        return
    create_database(server_conn)
    server_conn.close()

    db_conn = connect_to_prodev()
    if not db_conn:
        return
    create_table(db_conn)

    try:
        with open("user_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                insert_data(db_conn, {
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                })
    except FileNotFoundError:
        print("❌ user_data.csv file not found.")
    db_conn.close()
    print("🎉 Database seeding completed.")

if __name__ == "__main__":
    main()