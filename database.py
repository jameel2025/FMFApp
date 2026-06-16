import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        # مسار قاعدة البيانات
        try:
            from android.storage import app_storage_path
            self.db_path = os.path.join(app_storage_path(), "farm_management.db")
        except:
            self.db_path = os.path.join(os.path.expanduser("~"), "farm_management.db")
        
        self.init_database()
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الحسابات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT NOT NULL,
                account_number TEXT,
                balance REAL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المخزون
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                price REAL,
                category TEXT,
                unit TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                salary REAL,
                phone TEXT,
                email TEXT,
                hired_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الأعلاف
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feed_type TEXT NOT NULL,
                quantity REAL,
                price REAL,
                supplier TEXT,
                date_received TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # إدراج بيانات تجريبية
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, email, role)
                VALUES ('admin', '123456', 'admin@farm.com', 'مدير')
            ''')
            conn.commit()
        except:
            pass
        
        conn.close()
    
    def authenticate_user(self, username, password):
        """التحقق من بيانات المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2],
                "role": result[3]
            }
        return None
    
    def get_all_accounts(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_account(self, account_name, account_number, balance, description):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (account_name, account_number, balance, description)
            VALUES (?, ?, ?, ?)
        ''', (account_name, account_number, balance, description))
        conn.commit()
        conn.close()
    
    def get_all_inventory(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_inventory_item(self, item_name, quantity, price, category, unit):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (item_name, quantity, price, category, unit)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_name, quantity, price, category, unit))
        conn.commit()
        conn.close()
    
    def get_all_employees(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_employee(self, name, position, salary, phone, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, position, salary, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, position, salary, phone, email))
        conn.commit()
        conn.close()