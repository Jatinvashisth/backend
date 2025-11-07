import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def create_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQL_PORT")
        )
        if connection.is_connected():
            print("✅ Connected to MySQL Database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# Optional: Test connection when running directly
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("📂 You're connected to database:", record)
        cursor.close()
        conn.close()
