import sqlite3
from abc import ABC, abstractmethod
import threading

class MCPDatabaseConnection(ABC):

    @abstractmethod
    def connect(self):
        """Establish connection to the database"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params=None):
        """Execute a query against the database"""
        pass
    
    @abstractmethod
    def close(self):
        """Close the database connection"""
        pass

class SQLiteMCPConnection(MCPDatabaseConnection):

    def __init__(self, db_path: str = "company.db"):
        self.db_path = db_path
        self.local = threading.local()  # Thread-local storage
    
    def connect(self):
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path)
        return self.local.connection
    
    def execute_query(self, query: str, params=None):
        """Execute a query against the SQLite database in the current thread"""
        if not hasattr(self.local, 'connection'):
            self.connect()
        
        cursor = self.local.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            # Return results as list of dictionaries
            return [dict(zip(column_names, row)) for row in results]
        else:
            # For INSERT, UPDATE, DELETE queries, commit and return affected row count
            self.local.connection.commit()
            return cursor.rowcount
    
    def close(self):
        """Close the database connection for the current thread"""
        if hasattr(self.local, 'connection'):
            self.local.connection.close()
            delattr(self.local, 'connection')

class MCPEmployeeTool:
    """
    MCP (Model Context Protocol) Tool for employee-related database operations
    """
    def __init__(self, db_connection: MCPDatabaseConnection = None):
        self.db = db_connection or SQLiteMCPConnection()
        self.db.connect()
    
    def get_by_department(self, department: str):
        """Fetch employee details where department = 'AI' (or other department)"""
        query = "SELECT name, role, salary FROM employees WHERE department = ?"
        return self.db.execute_query(query, (department,))
    
    def get_all_employees(self):
        """Fetch all employees from the database"""
        query = "SELECT name, department, role, salary FROM employees"
        return self.db.execute_query(query)
    
    def get_count_of_employees(self):
        """Get the total count of employees"""
        query = "SELECT COUNT(*) as count FROM employees"
        result = self.db.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_employee_names_with_roles(self):
        """Get employee names with their roles"""
        query = "SELECT name, role FROM employees"
        return self.db.execute_query(query)
    
    def get_employee_names_with_projects(self):
        """Get employee names with their projects"""
        query = """
            SELECT e.name, e.role, p.name as project_name
            FROM employees e
            LEFT JOIN projects p ON e.department = p.department
        """
        return self.db.execute_query(query)
    
    def get_employee_names_with_salaries(self):
        """Get employee names with their salaries"""
        query = "SELECT name, salary FROM employees"
        return self.db.execute_query(query)
    
    def get_all_employee_names(self):
        """Get all employee names"""
        query = "SELECT name FROM employees"
        return self.db.execute_query(query)
    
    def get_all_employee_roles(self):
        """Get all distinct employee roles"""
        query = "SELECT DISTINCT role FROM employees"
        return self.db.execute_query(query)
    
    def get_all_employee_salaries(self):
        """Get all employee salaries"""
        query = "SELECT name, salary FROM employees"
        return self.db.execute_query(query)
    
    def get_all_employee_departments(self):
        """Get all distinct employee departments"""
        query = "SELECT DISTINCT department FROM employees"
        return self.db.execute_query(query)
    
    def get_all_projects(self):
        """Get all projects"""
        query = "SELECT name, department FROM projects"
        return self.db.execute_query(query)
    
    def get_all_issues(self):
        """Get all issues"""
        query = """
            SELECT i.title, i.status, i.project_id, p.name as project_name, p.department
            FROM issues i
            LEFT JOIN projects p ON i.project_id = p.id
        """
        return self.db.execute_query(query)
    
    def get_employees_by_role(self, role: str):
        """Get employees by role"""
        query = "SELECT name, department, salary FROM employees WHERE role LIKE ?"
        return self.db.execute_query(query, (f"%{role}%",))
    
    def get_employees_by_salary_range(self, min_salary: int, max_salary: int):
        """Get employees by salary range"""
        query = "SELECT name, department, role FROM employees WHERE salary BETWEEN ? AND ?"
        return self.db.execute_query(query, (min_salary, max_salary))
    
    def get_project_by_department(self, department: str):
        """Get projects by department"""
        query = "SELECT name FROM projects WHERE department = ?"
        return self.db.execute_query(query, (department,))
    
    def get_issues_by_status(self, status: str):
        """Get issues by status"""
        query = """
            SELECT i.title, i.project_id, i.status, p.name as project_name
            FROM issues i
            LEFT JOIN projects p ON i.project_id = p.id
            WHERE i.status = ?
        """
        return self.db.execute_query(query, (status,))
    
    def get_employee_by_name(self, name: str):
        """Get employee by name"""
        query = "SELECT name, department, role, salary FROM employees WHERE name LIKE ?"
        return self.db.execute_query(query, (f"%{name}%",))
    
    def get_issues_by_employee_department(self, employee_name: str):
        """Get issues related to the department where the employee works"""
        # First get the department of the employee
        dept_query = "SELECT department FROM employees WHERE name LIKE ?"
        dept_result = self.db.execute_query(dept_query, (f"%{employee_name}%",))
        
        if dept_result:
            department = dept_result[0]['department']
            # Now get issues related to projects in that department
            query = """
                SELECT i.title, i.status, i.project_id, p.name as project_name
                FROM issues i
                JOIN projects p ON i.project_id = p.id
                WHERE p.department = ?
            """
            return self.db.execute_query(query, (department,))
        else:
            return []
    
    def get_projects_by_employee_name(self, employee_name: str):
        """Get projects related to the department where the employee works"""
        # First get the department of the employee
        dept_query = "SELECT department FROM employees WHERE name LIKE ?"
        dept_result = self.db.execute_query(dept_query, (f"%{employee_name}%",))
        
        if dept_result:
            department = dept_result[0]['department']
            # Now get projects in that department
            query = "SELECT name FROM projects WHERE department = ?"
            return self.db.execute_query(query, (department,))
        else:
            return []
    
    def close_connection(self):
        """Close the database connection"""
        self.db.close()