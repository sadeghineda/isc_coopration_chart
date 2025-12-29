"""
Database module for Organization Chart - SQL Server Edition
اتصال به SQL Server با Windows Authentication
"""
import pyodbc
from typing import List, Dict, Optional

# SQL Server Connection Settings
SERVER = "MIS21"
DATABASE = "EmployeeStaging"
TABLE = "dbo.Employee_CHT"


def get_connection():
    """Get SQL Server connection with Windows Authentication"""
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"Trusted_Connection=yes;"  # Windows Authentication
    )
    return pyodbc.connect(connection_string)


def get_all_employees() -> List[Dict]:
    """Get all employees from database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # این کوئری رو بر اساس ستون‌های واقعی جدولت تغییر بده
    query = f"""
        SELECT 
            e.id,
            e.name,
            e.title,
            e.department,
            e.manager_id,
            e.email,
            e.phone,
            m.name as manager_name
        FROM {TABLE} e
        LEFT JOIN {TABLE} m ON e.manager_id = m.id
        ORDER BY e.id
    """
    
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    
    employees = []
    for row in cursor.fetchall():
        employees.append(dict(zip(columns, row)))
    
    conn.close()
    return employees


def get_employee_by_id(employee_id: int) -> Optional[Dict]:
    """Get single employee by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"SELECT * FROM {TABLE} WHERE id = ?"
    cursor.execute(query, (employee_id,))
    
    row = cursor.fetchone()
    if row:
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, row))
    else:
        result = None
    
    conn.close()
    return result


def get_departments() -> List[str]:
    """Get list of all departments"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"SELECT DISTINCT department FROM {TABLE} ORDER BY department"
    cursor.execute(query)
    
    departments = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return departments


def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return True, "اتصال موفق!"
    except Exception as e:
        return False, str(e)


def get_table_columns() -> List[str]:
    """Get column names from the table (برای دیباگ)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"SELECT TOP 1 * FROM {TABLE}"
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    conn.close()
    
    return columns


if __name__ == "__main__":
    # تست اتصال
    success, message = test_connection()
    print(f"Connection Test: {message}")
    
    if success:
        print("\nTable Columns:")
        columns = get_table_columns()
        for col in columns:
            print(f"  - {col}")
