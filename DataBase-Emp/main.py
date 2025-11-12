# how to integrate this with try and except blocks
# how to make this code reusable functions or classes
# how to log the operations performed

import sqlite3
import datetime

def log_and_time(func):
    def wrapper(*args,**kwargs):
        start_time = datetime.datetime.now()
        print(f"Function '{func.__name__}' started at {start_time}")
        result = func(*args,**kwargs)
        end_time = datetime.datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        with open('app_log.txt', 'a') as f:
            f.write(f"{start_time} - Function '{func.__name__}' executed in {execution_time}s\n")
        print(f"Function '{func.__name__}' executed in {execution_time}s")
        return result
    return wrapper

def connect_db(db_name):
    try:
        conn = sqlite3.connect(db_name)  
        print("Database connected successfully.")
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f'Database connection failed: {e}')
        return None, None

def close_db(conn):
    try:
        conn.close()
        print("Database connection closed successfully.")
    except Exception as e:
        print(f'Database connection failed to close: {e}')
        return None
        
@log_and_time
def create_employee_table(cursor, conn):
    print("Creating employee table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            department TEXT
        )
    ''')
    conn.commit()
    print("Employee table created successfully.")

@log_and_time
def insert_employee(cursor, conn, name, age, department):
    print("Inserting employee data...")
    cursor.execute('''
        INSERT INTO employees (name, age, department)
        VALUES (?, ?, ?)
    ''', (name, age, department))
    conn.commit()
    print("Employee data inserted successfully.")


@log_and_time
def fetch_employees(cursor):
    print("Fetching employee data...")
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    print(f"Employee data fetched successfully. {len(rows)} record(s) found.")
    return rows

@log_and_time
def update_employee(cursor, conn, emp_id, name=None, age=None, department=None):
    print("Updating employee data...")

    sql = f"UPDATE employees SET age = {age} WHERE id = {emp_id}"
    cursor.execute(sql  )
    conn.commit()
    print("Employee data updated successfully.")


@log_and_time
def delete_employee(cursor, conn, emp_id):
    print("Deleting employee data...")
    cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
    conn.commit()
    print("Employee data deleted successfully.")

db_name = 'emp.db'
conn, cursor = connect_db(db_name)
if conn and cursor:
    create_employee_table(cursor, conn)
    while True:
        print("\nDatabase Management System - Employee")
        print("1. Insert Employee")
        print("2. Fetch Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            name = input("Enter employee name: ")
            age = int(input("Enter employee age: "))
            department = input("Enter employee department: ")
            insert_employee(cursor, conn, name, age, department)
        elif choice == '2':
            rows = fetch_employees(cursor)
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No employee records available.")
        elif choice == '3':
            emp_id = int(input("Enter employee ID: "))
            name = input("Enter new employee name (press enter to skip): ")
            age = input("Enter new employee age (press enter to skip): ")
            department = input("Enter new employee department (press enter to skip): ")
            update_employee(cursor, conn, emp_id, name if name else None, int(age) if age else None, department if department else None)
        elif choice == '4':
            emp_id = int(input("Enter employee ID: "))
            delete_employee(cursor, conn, emp_id)
        elif choice == '5':
            close_db(conn)
            break
        else:
            print("Invalid choice. Please try again.")