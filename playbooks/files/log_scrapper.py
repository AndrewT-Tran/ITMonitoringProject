import os
import mysql.connector

LOG_FILE = "/var/log/syslog"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "logs_db",
}

def store_logs():
    with mysql.connector.connect(**DB_CONFIG) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INT AUTO_INCREMENT PRIMARY KEY, log TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        
        with open(LOG_FILE, "r") as file:
            for line in file:
                cursor.execute("INSERT INTO logs (log) VALUES (%s)", (line,))
        
        conn.commit()

store_logs()