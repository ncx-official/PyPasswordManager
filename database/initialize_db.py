import sqlite3
import os

# SQL Tables
PROFILES_TABLE = """
CREATE TABLE IF NOT EXISTS Profiles (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    master_password TEXT NOT NULL, -- Store hashed password
    salt TEXT, -- Optional for password hashing
    secret_question TEXT,
    secret_answer TEXT, -- Store hashed answer
    mfa_secret TEXT,
    failed_attempts INTEGER DEFAULT 0, -- To track login failures
    is_locked BOOLEAN DEFAULT 0, -- Account lock status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

PASSWORDS_TABLE = """
CREATE TABLE IF NOT EXISTS Passwords (
    password_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service_name TEXT NOT NULL,
    login_url TEXT,
    username_or_email TEXT NOT NULL,
    encrypted_password TEXT NOT NULL,
    notes TEXT,
    last_accessed TIMESTAMP,
  	password_strength INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Profiles (user_id) ON DELETE CASCADE
);
"""

EVENTLOG_TABLE = """
CREATE TABLE IF NOT EXISTS EventLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL, -- e.g., "Login", "Logout", "New User", "Password Created"
    category TEXT, -- e.g., "Authentication", "Management"
    details TEXT, -- Optional field for additional context (e.g., service name, reason for deletion)
    FOREIGN KEY (user_id) REFERENCES Profiles (user_id) ON DELETE CASCADE
);
"""

ENCRYPTEDKEYS_TABLE = """
CREATE TABLE IF NOT EXISTS EncryptedKeys (
    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    key_material TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Profiles (user_id) ON DELETE CASCADE
);
"""

BACKUPCODES_TABLE = """
CREATE TABLE IF NOT EXISTS BackupCodes (
    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    is_used BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Profiles (user_id) ON DELETE CASCADE
);
"""

SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS Sessions (
    session_id TEXT PRIMARY KEY, -- UUID or unique token as session ID
    user_id INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Profiles (user_id) ON DELETE CASCADE
);
"""

def initialize_database(db_path, db_name):
    global CREATE_USERS_TABLE, CREATE_PASSWORDS_TABLE, CREATE_MFA_LOG

    full_path = os.path.join(db_path, db_name)
    
    if os.path.exists(full_path):
        return f"Database '{db_name}' already exists at '{db_path}'."
    
    try:
        # Connect to the database
        connect = sqlite3.connect(full_path)
        cursor = connect.cursor()

        # Create tables
        cursor.execute(PROFILES_TABLE)
        cursor.execute(PASSWORDS_TABLE)
        cursor.execute(EVENTLOG_TABLE)
        cursor.execute(ENCRYPTEDKEYS_TABLE)
        cursor.execute(BACKUPCODES_TABLE)
        cursor.execute(SESSIONS_TABLE)

        # Commit changes and close connection
        connect.commit()
        connect.close()
        return f"Database '{db_name}' created successfully at '{db_path}'."

    except sqlite3.Error as e:
        return f"An error occurred while initializing the database: {e}"