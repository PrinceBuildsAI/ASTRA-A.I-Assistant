# import sqlite3

# conn = sqlite3.connect("astra.db")
# cursor = conn.cursor

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)
import csv
import sqlite3

con = sqlite3.connect("astra.db")
cursor = con.cursor()   # ✅

# query = """
# CREATE TABLE IF NOT EXISTS sys_command(
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     path VARCHAR(1000)
# )
# """
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'zoom', 'C:\\Users\\singh\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe')"
# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# query = "INSERT INTO sys_command VALUES (null,'chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')"
# cursor.execute(query)
# con.commit()


# cursor.execute("DELETE FROM web_command WHERE id = ?", (2,))
# con.commit() 
# cursor.execute("DELETE FROM contacts")
# con.commit()

# query = """
# CREATE TABLE IF NOT EXISTS web_command(
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     url VARCHAR(1000)  
# )
# """
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# query = "INSERT INTO web_command VALUES (null,'Linkedin', 'https://www.linkedin.com/feed/')"
# query = "INSERT INTO web_command VALUES (null,'canva', 'https://www.canva.in/')"
# cursor.execute(query)

# con.commit()

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255), address VARCHAR(225) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
# con.commit()
# con.close()

# Adding personal info table
# query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
# cursor.execute(query)

# Add Column in contacts table
# cursor.execute("ALTER TABLE contacts ADD COLUMN address VARCHAR(255)")

