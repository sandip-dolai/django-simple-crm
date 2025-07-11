import mysql.connector

# First, connect without specifying the database
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

# Prepare cursor object
cursor = dataBase.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS sample_crm_db")

print("Database created successfully!")

# Now connect to the newly created database
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sample_crm_db"
)

cursor = dataBase.cursor()
