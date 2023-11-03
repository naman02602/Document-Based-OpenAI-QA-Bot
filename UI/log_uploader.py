import pymysql
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from logging_config import logger
import os

# It's good practice to keep configuration settings like DATABASE_URL outside of the function
DATABASE_URL = os.getenv("DATABASE_URL")


def upload_logs_to_gcp():
    engine = create_engine(DATABASE_URL)

    # The get_db function is not used in your original code
    # It's defined but never called, so I have removed it

    # Create a new session for interacting with the database
    db = Session(bind=engine)

    try:
        # Read the log file
        with open("app.log", "r") as file:
            log_entries = file.readlines()

        # Parse and upload each log entry
        for entry in log_entries:
            # Assume each log entry is a single line
            # You may need to adjust the parsing based on the actual format of your log entries
            timestamp, name, level, message = entry.strip().split(" - ", 3)

            # Construct the SQL query using SQLAlchemy's text function to help prevent SQL injection
            query = text(
                f"INSERT INTO logs (timestamp, name, level, message) VALUES (:timestamp, :name, :level, :message)"
            )
            values = {
                "timestamp": timestamp,
                "name": name,
                "level": level,
                "message": message,
            }

            # Start a new transaction
            db.begin()
            db.execute(query, values)  # Execute the custom INSERT statement
            db.commit()  # Commit the transaction after each log entry to ensure data integrity

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()  # Rollback the transaction in case of an error

    finally:
        # Close the database session
        db.close()