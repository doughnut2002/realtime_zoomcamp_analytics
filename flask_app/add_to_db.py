import psycopg2

# Add your PostgreSQL database connection details
DB_HOST = 'Shekhar-IQ-postgres'
DB_NAME = 'de_data'
DB_USER = 'root'
DB_PASSWORD = 'shekhar'



def insert_into_database(module_name, module_id, email, time_spent_homework, time_spent_lectures, scores):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
   
    # Define your SQL query to insert data into the database
    sql = """INSERT INTO form_submissions (module_name, module_id, email, time_spent_homework, time_spent_lectures, scores)
             VALUES (%s, %s, %s, %s, %s, %s)"""
   
    # Execute the SQL query with the form data as parameters
    cursor.execute(sql, (module_name, module_id, email, time_spent_homework, time_spent_lectures, scores))
   
    # Commit the transaction
    conn.commit()
   
    # Close the cursor and connection
    cursor.close()
    conn.close()
