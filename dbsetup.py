import sqlite3

# Connect to SQLite (creates finance.db in the notebook environment)
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

#drop DB
cursor.execute("DROP TABLE IF EXISTS finance")

# Create finance table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS finance (
                    id INTEGER PRIMARY KEY,
                    company TEXT,
                    revenue REAL,
                    profit REAL,
                    stock_price REAL,
                    user_role TEXT
                )''')

# Insert 10 sample records
financial_data = [
    ('IBM', 75000, 5000, 145.32,'restricted'),
    ('Apple', 394000, 99900, 179.95,'restricted'),
    ('Microsoft', 211000, 72000, 314.10,'restricted'),
    ('Google', 280000, 76000, 2801.12,'restricted'),
    ('Amazon', 502000, 33000, 142.92,'restricted'),
    ('Meta', 117000, 39000, 302.56,'restricted'),
    ('Tesla', 123000, 15500, 199.35,'public'),
    ('Netflix', 35000, 5400, 412.75,'public'),
    ('Nvidia', 26000, 9600, 450.99,'public'),
    ('Samsung', 244000, 41000, 70.10,'public')
]

# Clear existing records (optional)
#cursor.execute("DELETE FROM finance")

# Insert new records
cursor.executemany("INSERT INTO finance (company, revenue, profit, stock_price,user_role) VALUES (?, ?, ?, ?, ?)", financial_data)
conn.commit()
conn.close()

print("✅ SQLite database 'finance.db' is set up with 10 records!")

import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM finance")
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)  # Prints all records
