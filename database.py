import sqlite3
import hashlib
import base64
import bcrypt
import jwt
import datetime

jwt_secret = "uDQ1l5_aq_nFYV0YEPNLOSWoFgTzrp_de"
jwt_token_weeks_limit = 5

# Database initialization
def init_database():
    """Creates database and tables if they don't exist"""
    conn = sqlite3.connect('OprosDataBase.db')
    cursor = conn.cursor()
    
    # Create tables with updated structure
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        username STRING UNIQUE NOT NULL,
        password STRING NOT NULL,
        [group] STRING NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        task_theme STRING NOT NULL,
        task_name STRING NOT NULL,
        task_text STRING NOT NULL,
        task_number INTEGER NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Options (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        task_id INTEGER REFERENCES Tasks (id) NOT NULL,
        option_letter STRING NOT NULL,
        option_text STRING NOT NULL,
        is_correct BOOLEAN NOT NULL,
        UNIQUE (
            task_id,
            option_letter
        )
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answers (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        username_id INTEGER REFERENCES Users (id) NOT NULL,
        task_id INTEGER REFERENCES Tasks (id) NOT NULL,
        selected_options STRING NOT NULL,
        result BOOLEAN NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

class DatabaseManager:
    def __init__(self, db_name='OprosDataBase.db'):
        self.db_name = db_name
        init_database()

    def check_jwt_token(self, token):
        try:
            decoded = jwt.decode(token, jwt_secret, algorithms=["HS256"])

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if decoded["group"]:
                cursor.execute(
                    "SELECT id, username, [group] FROM Users WHERE id=? AND username=? AND [group]=?",
                    (decoded["id"], decoded["username"], decoded["group"])
                )
            else:
                cursor.execute(
                    "SELECT id, username, [group] FROM Users WHERE id=? AND username=?",
                    (decoded["username"],)
                )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return decoded
            else:
                return None
        except jwt.ExpiredSignatureError:
            print("Срок действия токена истёк")
            return None
        except jwt.InvalidSignatureError:
            print("Недействительная подпись токена")
            return None
        except jwt.InvalidTokenError:
            print("Недействительный токен")
            return None
    
    def authenticate_user(self, username, password, group=None):
        """Authenticate user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if group:
                cursor.execute(
                    "SELECT id, username, password, [group] FROM Users WHERE username=? AND [group]=?",
                    (username, group)
                )
            else:
                cursor.execute(
                    "SELECT id, username, password, [group] FROM Users WHERE username=?",
                    (username,)
                )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), user[2]):
                    payload = {"id": user[0], "username": user[1], "group": user[3], "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(weeks=jwt_token_weeks_limit)}
                    return jwt.encode(payload, jwt_secret, algorithm="HS256")
                else:
                    return None
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def register_user(self, username, password, group):
        """Register new user"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM Users WHERE username=?", (username,))
            if cursor.fetchone():
                conn.close()
                return {'success': False, 'error': 'Пользователь уже существует'}

            hashed = bcrypt.hashpw(
                base64.b64encode(hashlib.sha256(password.encode()).digest()),
                bcrypt.gensalt()
            )
            
            # Add new user
            cursor.execute(
                "INSERT INTO Users (username, password, [group]) VALUES (?, ?, ?)",
                (username, hashed, group)
            )
            
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Регистрация успешна!'}
        except Exception as e:
            print(f"Registration error: {e}")
            return {'success': False, 'error': str(e)}
    
    def save_test_result(self, user_id, task_id, answers, result):
        """Save test result"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get max ID for Answers
            cursor.execute("SELECT MAX(id) FROM Answers")
            max_id = cursor.fetchone()[0] or 0
            
            cursor.execute(
                '''INSERT INTO Answers (id, username_id, task_id, selected_options, result) 
                   VALUES (?, ?, ?, ?, ?)''',
                (max_id + 1, user_id, task_id, answers, result)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Save test result error: {e}")
            return False
    
    def get_tasks(self):
        """Get list of all tasks"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, task_name, task_theme, task_number FROM Tasks ORDER BY task_number")
            tasks = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': task[0],
                    'name': task[1],
                    'theme': task[2],
                    'number': task[3]
                }
                for task in tasks
            ]
        except Exception as e:
            print(f"Get tasks error: {e}")
            return []
    
    def get_task_by_id(self, task_id):
        """Get task by ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, task_theme, task_name, task_text, task_number FROM Tasks WHERE id=?",
                (task_id,)
            )
            task = cursor.fetchone()
            conn.close()
            
            if task:
                return {
                    'id': task[0],
                    'theme': task[1],
                    'name': task[2],
                    'text': task[3],
                    'number': task[4]
                }
            return None
        except Exception as e:
            print(f"Get task error: {e}")
            return None
        
    def get_answers_by_task(self, task_id):
        """Get answers by task ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, option_letter, option_text, is_correct FROM Options WHERE task_id=? ORDER BY option_letter",
                (task_id,)
            )
            answers = cursor.fetchall()
            conn.close()
            
            if answers:
                object_answers = []
                for answer in answers:
                    object_answers.append({
                        'id': answer[0],
                        'option_letter': answer[1],
                        'option_text': answer[2],
                        'is_correct': answer[3]
                    })
                return object_answers
            return None
        except Exception as e:
            print(f"Get task error: {e}")
            return None
    
    def get_user_results(self, user_id):
        conn = sqlite3.connect(self.db_name)
        """Get user results"""
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT t.task_name, t.task_theme, a.result, a.selected_options
                FROM Answers a
                JOIN Tasks t ON a.task_id = t.id
                WHERE a.username_id = ?
                ORDER BY t.task_number
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'task_name': r[0],
                    'theme': r[1],
                    'result': 'Correct' if r[2] else 'Incorrect',
                    'answers': r[3]
                }
                for r in results
            ]
        except Exception as e:
            print(f"Get user results error: {e}")
            conn.close()
            return []
    
    # НОВЫЕ ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ ДАННЫМИ
    def insert_test_data(self):
        """Insert test data into database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            print("\nInserting test data...")
            
            # Clear existing data first
            self.clear_all_data()
            
            # Insert test tasks (same as before)
            test_tasks = [
                ('Mathematics', 'Fraction Addition', 'A,B,C', 'Add fractions 1/2 + 1/3', 1),
                ('Physics', 'Newtons Laws', 'B,D,A', 'State Newtons first law', 2),
                ('Programming', 'Python Basics', 'C,A,B', 'What is a list in Python?', 3)
            ]
            
            cursor.executemany(
                "INSERT INTO Tasks (task_theme, task_name, true_answers, task_text, task_number) VALUES (?, ?, ?, ?, ?)",
                test_tasks
            )
            
            conn.commit()
            conn.close()
            print("Test data inserted successfully!")
            return True
            
        except Exception as e:
            print(f"Error inserting test data: {e}")
            return False
    
    def clear_all_data(self):
        """Clear all data from database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Disable foreign keys
            cursor.execute("PRAGMA foreign_keys = OFF")
            
            # Clear tables
            cursor.execute("DELETE FROM Answers")
            cursor.execute("DELETE FROM Tasks")
            cursor.execute("DELETE FROM Users")
            
            # Reset auto-increment
            cursor.execute("DELETE FROM sqlite_sequence")
            
            # Enable foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            stats = {}
            tables = ['Users', 'Tasks', 'Answers']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            
            conn.close()
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

# Create database instance
db = DatabaseManager()