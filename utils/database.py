import sqlite3
import json
import pandas as pd
from datetime import datetime
import os
from config import DB_PATH

class DatabaseManager:
    """Centralized database manager for SEO Generator"""
    
    def __init__(self, db_path=DB_PATH):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self._ensure_directory_exists()
        self.init_db()
    
    def _ensure_directory_exists(self):
        """Ensure the directory for the database exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            template_id TEXT,
            primary_keyword TEXT,
            category TEXT,
            audience TEXT,
            secondary TEXT,
            prompt_text TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            type TEXT,
            category TEXT,
            usage_count INTEGER DEFAULT 0,
            last_used TEXT,
            source TEXT
        )
        ''')
        
        # Add other tables from your existing DatabaseManager
        
        conn.commit()
        conn.close()
    
    # Add the rest of your DatabaseManager methods here