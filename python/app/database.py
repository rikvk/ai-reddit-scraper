import sqlite3
import csv
import os
from datetime import datetime

# Function to create a connection to the SQLite database
def create_server_connection(project_name):
    try:
        connection = sqlite3.connect(f'sqlite/{project_name}.db')
        print("SQLite Database connection successful")
        create_table_if_not_exists(connection, project_name)
        return connection
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
        return None

# Function to execute a query in the SQLite database
def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

# Function that will check if a submission already exists in the database
def check_if_submission_already_in_db(connection, external_id, project_name):
    query = f"SELECT EXISTS(SELECT 1 FROM {project_name} WHERE external_id = ?)"
    cursor = connection.cursor()
    cursor.execute(query, (external_id,))
    return cursor.fetchone()[0]

def create_table_if_not_exists(conn, project_name):
    # Check if table exists
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{project_name}'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        # Clear existing data
        cursor.execute(f"DELETE FROM {project_name}")
        conn.commit()
        print(f"Cleared existing data from table {project_name}")
    else:
        # Create new table
        create_table_query = f"""
        CREATE TABLE {project_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT,
            external_id TEXT,
            title TEXT,
            external_url TEXT,
            external_subreddit TEXT,
            content TEXT,
            meets_qualifier TEXT,
            generation TEXT,
            external_created DATETIME,
            date_created DATETIME,
            date_updated DATETIME
        );
        """
        try:
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Created new table {project_name}")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

def export_database_to_csv(connection, project_name):
    cursor = connection.cursor()
    query = f"SELECT * FROM {project_name}"
    cursor.execute(query)
    
    # Fetch all rows and column names
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    # Create the exports directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"exports/{project_name}_{timestamp}.csv"
    
    # Write to CSV file
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(column_names)
        csv_writer.writerows(rows)
    
    print(f"Database exported to {filename}")
