"""
Model Context Protocol (MCP) Framework for LLM-Database interaction
"""
import sqlite3
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum


class QueryType(Enum):
    """Enumeration of supported query types"""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class MCPConnection(ABC):
    """
    Abstract base class for MCP (Model Context Protocol) database connections.
    Defines the interface for LLM-database interactions without exposing credentials.
    """
    
    @abstractmethod
    def connect(self):
        """Establish connection to the database"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query against the database and return results as dictionaries"""
        pass
    
    @abstractmethod
    def close(self):
        """Close the database connection"""
        pass


class SQLiteMCPConnection(MCPConnection):
    """
    SQLite implementation of the Model Context Protocol.
    Provides secure database access for LLMs without exposing credentials.
    """
    def __init__(self, db_path: str = "company.db"):
        self.db_path = db_path
        self.local = threading.local()  # Thread-local storage for connection safety
    
    def connect(self):
        """Establish connection to the SQLite database for the current thread"""
        if not hasattr(self.local, 'connection'):
            self.local.connection = sqlite3.connect(self.db_path)
            # Set row factory to return results as dictionaries
            self.local.connection.row_factory = sqlite3.Row
        return self.local.connection
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query against the SQLite database in the current thread"""
        if not hasattr(self.local, 'connection'):
            self.connect()
        
        cursor = self.local.connection.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # For SELECT queries, return the results
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                # Convert Row objects to dictionaries
                return [dict(row) for row in rows]
            else:
                # For INSERT, UPDATE, DELETE queries, commit and return affected row count
                self.local.connection.commit()
                return [{"affected_rows": cursor.rowcount}]
        except Exception as e:
            # Rollback on error
            self.local.connection.rollback()
            raise e
    
    def close(self):
        """Close the database connection for the current thread"""
        if hasattr(self.local, 'connection'):
            self.local.connection.close()
            delattr(self.local, 'connection')


class MCPDatabaseInterface:
    """
    MCP (Model Context Protocol) Database Interface for LLM interactions.
    Provides a secure, abstracted layer between LLMs and databases.
    """
    def __init__(self, connection: MCPConnection = None):
        self.connection = connection or SQLiteMCPConnection()
        self.connection.connect()
    
    def fetch_employee_details_by_department(self, department: str) -> List[Dict[str, Any]]:
        """
        MCP-protected query to fetch employee details by department.
        Example: Fetch employee details where department = 'AI'
        """
        query = "SELECT name, role, salary FROM employees WHERE department = ?"
        return self.connection.execute_query(query, (department,))
    
    def fetch_all_employees(self) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch all employees"""
        query = "SELECT name, department, role, salary FROM employees"
        return self.connection.execute_query(query)
    
    def fetch_employees_by_role(self, role: str) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch employees by role"""
        query = "SELECT name, department, salary FROM employees WHERE role LIKE ?"
        return self.connection.execute_query(query, (f"%{role}%",))
    
    def fetch_projects_by_department(self, department: str) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch projects by department"""
        query = "SELECT name FROM projects WHERE department = ?"
        return self.connection.execute_query(query, (department,))
    
    def fetch_issues_by_status(self, status: str) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch issues by status"""
        query = """
            SELECT i.title, i.project_id, p.name as project_name
            FROM issues i
            LEFT JOIN projects p ON i.project_id = p.id
            WHERE i.status = ?
        """
        return self.connection.execute_query(query, (status,))
    
    def fetch_employee_by_name(self, name: str) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch employee by name"""
        query = "SELECT name, department, role, salary FROM employees WHERE name LIKE ?"
        return self.connection.execute_query(query, (f"%{name}%",))
    
    def fetch_issues_by_employee(self, name: str) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch issues related to an employee based on department"""
        # First, get the employee's department
        emp_query = "SELECT department FROM employees WHERE name LIKE ?"
        employee = self.connection.execute_query(emp_query, (f"%{name}%",))
        
        if employee:
            dept = employee[0]['department']
            # Then find issues in projects related to that department
            query = '''SELECT i.title, i.status, i.project_id, p.name as project_name
                       FROM issues i
                       LEFT JOIN projects p ON i.project_id = p.id
                       WHERE p.department = ?'''
            return self.connection.execute_query(query, (dept,))
        else:
            return []
    
    def fetch_all_projects(self) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch all projects"""
        query = "SELECT name, department FROM projects"
        return self.connection.execute_query(query)
    
    def fetch_all_issues(self) -> List[Dict[str, Any]]:
        """MCP-protected query to fetch all issues"""
        query = """
            SELECT i.title, i.status, i.project_id, p.name as project_name, p.department
            FROM issues i
            LEFT JOIN projects p ON i.project_id = p.id
        """
        return self.connection.execute_query(query)
    
    def get_employee_count(self) -> int:
        """MCP-protected query to get employee count"""
        query = "SELECT COUNT(*) as count FROM employees"
        result = self.connection.execute_query(query)
        return result[0]['count'] if result else 0
    
    def close_connection(self):
        """Close the MCP database connection"""
        self.connection.close()


class MCPLLMInterface:
    """
    MCP (Model Context Protocol) Interface for LLM interactions.
    Provides a secure way for LLMs to query databases without direct credential access.
    """
    def __init__(self, db_interface: MCPDatabaseInterface = None):
        self.db_interface = db_interface or MCPDatabaseInterface()
    
    def execute_structured_query(self, query_type: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a structured query based on LLM interpretation of natural language.
        This method ensures safe, parameterized queries without SQL injection risk.
        """
        if query_type.lower() == "employees_by_department":
            department = filters.get("department", "")
            return self.db_interface.fetch_employee_details_by_department(department)
        elif query_type.lower() == "employees_by_role":
            role = filters.get("role", "")
            return self.db_interface.fetch_employees_by_role(role)
        elif query_type.lower() == "projects_by_department":
            department = filters.get("department", "")
            return self.db_interface.fetch_projects_by_department(department)
        elif query_type.lower() == "issues_by_status":
            status = filters.get("status", "")
            return self.db_interface.fetch_issues_by_status(status)
        elif query_type.lower() == "employee_by_name":
            name = filters.get("name", "")
            return self.db_interface.fetch_employee_by_name(name)
        elif query_type.lower() == "issues_by_employee":
            name = filters.get("name", "")
            return self.db_interface.fetch_issues_by_employee(name)
        elif query_type.lower() == "all_employees":
            return self.db_interface.fetch_all_employees()
        elif query_type.lower() == "all_projects":
            return self.db_interface.fetch_all_projects()
        elif query_type.lower() == "all_issues":
            return self.db_interface.fetch_all_issues()
        else:
            # Default to all employees if unknown query type
            return self.db_interface.fetch_all_employees()
    
    def get_db_stats(self) -> Dict[str, Any]:
        """Get database statistics through MCP interface"""
        stats = {}
        stats['employee_count'] = self.db_interface.get_employee_count()
        stats['project_count'] = len(self.db_interface.fetch_all_projects())
        stats['issue_count'] = len(self.db_interface.fetch_all_issues())
        return stats
    
    def close(self):
        """Close the MCP interface"""
        self.db_interface.close_connection()


# Example usage for testing
if __name__ == "__main__":
    # Create MCP interface for LLM-database interaction
    mcp_interface = MCPLLMInterface()
    
    print("Testing MCP Framework:")
    
    ai_employees = mcp_interface.execute_structured_query(
        "employees_by_department", 
        {"department": "AI"}
    )
    print(f"AI Department Employees: {ai_employees}")
    
    # Get database stats
    stats = mcp_interface.get_db_stats()
    print(f"Database Stats: {stats}")
    
    # Close the interface
    mcp_interface.close()
    print("MCP Framework test completed successfully.")