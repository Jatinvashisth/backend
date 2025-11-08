import os
from dotenv import load_dotenv
import pymysql
from pymysql.err import MySQLError

# Load environment variables from .env file
load_dotenv()

def create_connection():
    """Create and return a MySQL database connection using PyMySQL."""
    connection = None
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Connected to MySQL Database via PyMySQL")
        return connection
    except MySQLError as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# Optional: Test connection when running directly
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("📂 You're connected to database:", record)
        finally:
            conn.close()
            print("🔒 MySQL connection closed.")
