import sqlite3

def init_db():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute('''DROP TABLE IF EXISTS employees''')
    cursor.execute('''DROP TABLE IF EXISTS projects''')
    cursor.execute('''DROP TABLE IF EXISTS issues''')
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    ''')
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    
    # Create issues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    
    # Insert sample employees - removing duplicates
    employees = [
        ('Aswin', 'AI', 'ML Engineer', 80000),
        ('Meena', 'AI', 'Data Scientist', 75000),
        ('Karthik', 'AI', 'GenAI Engineer', 90000),
        ('Priya', 'AI', 'AI Researcher', 85000),
        ('Rajesh', 'AI', 'Computer Vision Engineer', 82000),
        ('Swati', 'AI', 'NLP Specialist', 78000),
        ('Ravi', 'Backend', 'Python Developer', 60000),
        ('Sneha', 'Backend', 'Full Stack Developer', 65000),
        ('Vikram', 'Backend', 'Node.js Developer', 62000),
        ('Anjali', 'Backend', 'Java Developer', 68000),
        ('Manoj', 'Backend', 'API Specialist', 64000),
        ('Arjun', 'DevOps', 'Cloud Engineer', 70000),
        ('Deepika', 'DevOps', 'DevOps Specialist', 72000),
        ('Suresh', 'DevOps', 'Infrastructure Engineer', 68000),
        ('Neha', 'DevOps', 'Platform Engineer', 71000),
        ('Rahul', 'Sales', 'Sales Manager', 75000),
        ('Pooja', 'Sales', 'Account Executive', 55000),
        ('Amit', 'HR', 'HR Manager', 65000),
        ('Divya', 'HR', 'Recruitment Specialist', 50000),
        ('Komal', 'Marketing', 'Marketing Manager', 60000),
        ('Rohit', 'Marketing', 'Digital Marketing Specialist', 52000)
    ]
    
    cursor.executemany('INSERT INTO employees (name, department, role, salary) VALUES (?, ?, ?, ?)', employees)
    
    # Insert sample projects
    projects = [
        ('AI Model Development', 'AI'),
        ('Data Pipeline Optimization', 'AI'),
        ('Backend API Development', 'Backend'),
        ('Cloud Infrastructure Setup', 'DevOps'),
        ('Sales CRM System', 'Sales'),
        ('HR Portal Upgrade', 'HR'),
        ('Marketing Campaign Automation', 'Marketing')
    ]
    
    cursor.executemany('INSERT INTO projects (name, department) VALUES (?, ?)', projects)
    
    # Insert sample issues
    issues = [
        ('Bug in ML model prediction', 'Open', 1),
        ('Performance issue in data pipeline', 'In Progress', 2),
        ('API endpoint returning 500 error', 'Open', 3),
        ('Server downtime in production', 'Closed', 4),
        ('CRM sync issue', 'Open', 5),
        ('Portal login bug', 'In Progress', 6),
        ('Email delivery failure', 'Open', 7)
    ]
    
    cursor.executemany('INSERT INTO issues (title, status, project_id) VALUES (?, ?, ?)', issues)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data!")

if __name__ == "__main__":
    init_db()