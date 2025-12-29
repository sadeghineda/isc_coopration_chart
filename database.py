# """
# Database module for Organization Chart - SQL Server
# اتصال به SQL Server با Windows Authentication
# """
# import pyodbc
# from typing import List, Dict

# # SQL Server Connection Settings
# SERVER = "MIS21"
# DATABASE = "EmployeeStaging"
# TABLE = "dbo.Employee_CHT"


# def get_connection():
#     """Get SQL Server connection with Windows Authentication"""
#     connection_string = (
#         f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#         f"SERVER={SERVER};"
#         f"DATABASE={DATABASE};"
#         f"Trusted_Connection=yes;"
#     )
#     return pyodbc.connect(connection_string)


# def get_org_data() -> Dict:
#     """
#     Get organization hierarchy data
#     Returns: {
#         'ceo': str,
#         'deputies': {name: {'managers': {name: {'groups': [str]}}}}
#     }
#     """
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     query = f"""
#         SELECT DISTINCT
#             CEO_FullName,
#             Deputy_FullName,
#             Manager_FullName,
#             Group_FullName
#         FROM {TABLE}
#         WHERE CEO_FullName IS NOT NULL
#         ORDER BY Deputy_FullName, Manager_FullName, Group_FullName
#     """
    
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     conn.close()
    
#     # ساختار سلسله مراتبی
#     org = {
#         'ceo': None,
#         'deputies': {}
#     }
    
#     for row in rows:
#         ceo, deputy, manager, group = row
        
#         # مدیرعامل
#         if ceo:
#             org['ceo'] = ceo
        
#         # معاون‌ها
#         if deputy and deputy not in org['deputies']:
#             org['deputies'][deputy] = {'managers': {}}
        
#         # مدیرها
#         if deputy and manager:
#             if manager not in org['deputies'][deputy]['managers']:
#                 org['deputies'][deputy]['managers'][manager] = {'groups': []}
        
#         # گروه‌ها
#         if deputy and manager and group:
#             if group not in org['deputies'][deputy]['managers'][manager]['groups']:
#                 org['deputies'][deputy]['managers'][manager]['groups'].append(group)
    
#     return org


# def get_flat_data() -> List[Dict]:
#     """Get flat list of all records"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     query = f"""
#         SELECT DISTINCT
#             CEO_FullName,
#             Deputy_FullName,
#             Manager_FullName,
#             Group_FullName
#         FROM {TABLE}
#         ORDER BY Deputy_FullName, Manager_FullName, Group_FullName
#     """
    
#     cursor.execute(query)
#     columns = ['ceo', 'deputy', 'manager', 'group']
    
#     results = []
#     for row in cursor.fetchall():
#         results.append(dict(zip(columns, row)))
    
#     conn.close()
#     return results


# def get_stats() -> Dict:
#     """Get organization statistics"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     stats = {}
    
#     # تعداد معاونین
#     cursor.execute(f"SELECT COUNT(DISTINCT Deputy_FullName) FROM {TABLE} WHERE Deputy_FullName IS NOT NULL")
#     stats['deputies_count'] = cursor.fetchone()[0]
    
#     # تعداد مدیران
#     cursor.execute(f"SELECT COUNT(DISTINCT Manager_FullName) FROM {TABLE} WHERE Manager_FullName IS NOT NULL")
#     stats['managers_count'] = cursor.fetchone()[0]
    
#     # تعداد گروه‌ها
#     cursor.execute(f"SELECT COUNT(DISTINCT Group_FullName) FROM {TABLE} WHERE Group_FullName IS NOT NULL")
#     stats['groups_count'] = cursor.fetchone()[0]
    
#     conn.close()
#     return stats


# def test_connection():
#     """Test database connection"""
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT TOP 1 * FROM " + TABLE)
#         conn.close()
#         return True, "اتصال موفق!"
#     except Exception as e:
#         return False, str(e)


# if __name__ == "__main__":
#     success, msg = test_connection()
#     print(f"Test: {msg}")
    
#     if success:
#         stats = get_stats()
#         print(f"معاونین: {stats['deputies_count']}")
#         print(f"مدیران: {stats['managers_count']}")
#         print(f"گروه‌ها: {stats['groups_count']}")


"""
Database module for Organization Chart - SQL Server
اتصال به SQL Server با Windows Authentication
"""
import pyodbc
from typing import List, Dict

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
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)


def get_org_data() -> Dict:
    """
    Get organization hierarchy data
    Returns: {
        'ceo': str,
        'deputies': {name: {'managers': {name: {'groups': [str]}}}}
    }
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"""
        SELECT DISTINCT
            CEO_FullName,
            Deputy_FullName,
            Manager_FullName,
            Group_FullName
        FROM {TABLE}
        WHERE CEO_FullName IS NOT NULL
        ORDER BY Deputy_FullName, Manager_FullName, Group_FullName
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    # ساختار سلسله مراتبی
    org = {
        'ceo': None,
        'deputies': {}
    }
    
    for row in rows:
        ceo, deputy, manager, group = row
        
        # مدیرعامل
        if ceo:
            org['ceo'] = ceo
        
        # معاون‌ها
        if deputy and deputy not in org['deputies']:
            org['deputies'][deputy] = {'managers': {}}
        
        # مدیرها
        if deputy and manager:
            if manager not in org['deputies'][deputy]['managers']:
                org['deputies'][deputy]['managers'][manager] = {'groups': []}
        
        # گروه‌ها
        if deputy and manager and group:
            if group not in org['deputies'][deputy]['managers'][manager]['groups']:
                org['deputies'][deputy]['managers'][manager]['groups'].append(group)
    
    return org


def get_flat_data() -> List[Dict]:
    """Get flat list of all records"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = f"""
        SELECT DISTINCT
            CEO_FullName,
            Deputy_FullName,
            Manager_FullName,
            Group_FullName
        FROM {TABLE}
        ORDER BY Deputy_FullName, Manager_FullName, Group_FullName
    """
    
    cursor.execute(query)
    columns = ['ceo', 'deputy', 'manager', 'group']
    
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    conn.close()
    return results


def get_stats() -> Dict:
    """Get organization statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # تعداد معاونین
    cursor.execute(f"SELECT COUNT(DISTINCT Deputy_FullName) FROM {TABLE} WHERE Deputy_FullName IS NOT NULL")
    stats['deputies_count'] = cursor.fetchone()[0]
    
    # تعداد مدیران
    cursor.execute(f"SELECT COUNT(DISTINCT Manager_FullName) FROM {TABLE} WHERE Manager_FullName IS NOT NULL")
    stats['managers_count'] = cursor.fetchone()[0]
    
    # تعداد گروه‌ها
    cursor.execute(f"SELECT COUNT(DISTINCT Group_FullName) FROM {TABLE} WHERE Group_FullName IS NOT NULL")
    stats['groups_count'] = cursor.fetchone()[0]
    
    conn.close()
    return stats


def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 * FROM " + TABLE)
        conn.close()
        return True, "اتصال موفق!"
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    success, msg = test_connection()
    print(f"Test: {msg}")
    
    if success:
        stats = get_stats()
        print(f"معاونین: {stats['deputies_count']}")
        print(f"مدیران: {stats['managers_count']}")
        print(f"گروه‌ها: {stats['groups_count']}")