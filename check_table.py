"""
اسکریپت بررسی ساختار جدول
این رو اول اجرا کن تا ببینیم ستون‌های جدولت چیه
"""
import pyodbc

SERVER = "MIS21"
DATABASE = "EmployeeStaging"
TABLE = "dbo.Employee_CHT"

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

try:
    print("در حال اتصال به سرور...")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    print(f"✅ اتصال به {SERVER} موفق!\n")
    
    # گرفتن اطلاعات ستون‌ها
    print(f"📋 ستون‌های جدول {TABLE}:")
    print("-" * 50)
    
    cursor.execute(f"""
        SELECT 
            COLUMN_NAME, 
            DATA_TYPE, 
            IS_NULLABLE,
            CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'Employee_CHT' 
        AND TABLE_SCHEMA = 'dbo'
        ORDER BY ORDINAL_POSITION
    """)
    
    for row in cursor.fetchall():
        col_name, data_type, nullable, max_len = row
        len_info = f"({max_len})" if max_len else ""
        print(f"  {col_name}: {data_type}{len_info} {'NULL' if nullable == 'YES' else 'NOT NULL'}")
    
    # نمایش چند رکورد اول
    print(f"\n📊 نمونه داده (۵ ردیف اول):")
    print("-" * 50)
    
    cursor.execute(f"SELECT TOP 5 * FROM {TABLE}")
    columns = [col[0] for col in cursor.description]
    print(" | ".join(columns))
    print("-" * 50)
    
    for row in cursor.fetchall():
        print(" | ".join(str(val)[:20] if val else "NULL" for val in row))
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("حالا نام ستون‌های مربوط به چارت سازمانی رو بگو:")
    print("  - ستون ID کارمند کدومه؟")
    print("  - ستون نام کدومه؟")
    print("  - ستون سمت/عنوان شغلی کدومه؟")
    print("  - ستون دپارتمان کدومه؟")
    print("  - ستون ID مدیر (manager) کدومه؟")
    
except pyodbc.Error as e:
    print(f"❌ خطا در اتصال: {e}")
    print("\nراه حل‌های احتمالی:")
    print("1. مطمئن شو ODBC Driver 17 نصبه")
    print("2. نام سرور رو چک کن")
    print("3. دسترسی به سرور رو بررسی کن")