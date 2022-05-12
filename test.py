# Understanding sqlite database

import sqlite3

# Create a connection
connection = sqlite3.connect('database.db')

# Create a cursor(It helps in executing the sql queries)
cursor = connection.cursor()

# Create the table
create_table = "CREATE TABLE users (Id int, Username text, Password text)"
cursor.execute(create_table)

# Load some data
user = (1, 'bob', 'asdf')
insert_data = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_data, user)

#Loading multiple data at same time
users = [
    (2, 'jose', 'asdf1'),
    (3, 'angela', 'asdf2')
]

# Inseting many data
cursor.executemany(insert_data, users)

# Reading the table
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

#Commit and close the connection
connection.commit()
connection.close()