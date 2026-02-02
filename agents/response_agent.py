class ResponseAgent:
    def __init__(self):
        pass

    def format(self, query_analysis: dict, data: list):
        """
        Format the response based on query analysis and data
        """
        query_type = query_analysis.get("type", "unknown")
        parameter = query_analysis.get("parameter", "none")
        
        if query_type == "count_employees":
            count = data[0].get("count", 0) if data else 0
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": f"There are {count} employees in total.",
                "summary": "Employee count query results"
            }
        
        elif query_type == "all_employee_names":
            if data:
                names = [emp["name"] for emp in data if "name" in emp]
                names_list = "\n- ".join(names)
                formatted_response = f"Employee names in the organization:\n- {names_list}"
            else:
                formatted_response = "No employees found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee names query results"
            }
        
        elif query_type == "employees_by_department":
            if data:
                employees_list = []
                for emp in data:
                    name = emp.get("name", "Unknown")
                    role = emp.get("role", "Unknown")
                    salary = emp.get("salary", 0)
                    emp_str = f"{name}, {role}, ${salary:,}"
                    employees_list.append(emp_str)
                
                employees_formatted = "\n- ".join(employees_list)
                formatted_response = f"Employees in {parameter} department:\n- {employees_formatted}"
            else:
                formatted_response = f"No employees found in {parameter}."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee details by department query results"
            }
        
        elif query_type == "employee_names_with_roles":
            if data:
                employees_list = []
                for emp in data:
                    name = emp.get("name", "Unknown")
                    role = emp.get("role", "Unknown")
                    emp_str = f"{name}, {role}"
                    employees_list.append(emp_str)
                
                employees_formatted = "\n- ".join(employees_list)
                formatted_response = f"Employee names with roles:\n- {employees_formatted}"
            else:
                formatted_response = "No employees found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee names with roles query results"
            }
        
        elif query_type == "employee_names_with_salaries":
            if data:
                employees_list = []
                for emp in data:
                    name = emp.get("name", "Unknown")
                    salary = emp.get("salary", 0)
                    emp_str = f"{name}, ${salary:,}"
                    employees_list.append(emp_str)
                
                employees_formatted = "\n- ".join(employees_list)
                formatted_response = f"Employee names with salaries:\n- {employees_formatted}"
            else:
                formatted_response = "No employees found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee names with salaries query results"
            }
        
        elif query_type == "all_employees":
            if data:
                employees_list = []
                for emp in data:
                    name = emp.get("name", "Unknown")
                    dept = emp.get("department", "Unknown")
                    role = emp.get("role", "Unknown")
                    salary = emp.get("salary", 0)
                    emp_str = f"{name}, {role}, {dept}, ${salary:,}"
                    employees_list.append(emp_str)
                
                employees_formatted = "\n- ".join(employees_list)
                formatted_response = f"All employees in the organization:\n- {employees_formatted}"
            else:
                formatted_response = "No employees found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "All employees query results"
            }
        
        elif query_type == "employee_by_name":
            if data:
                emp = data[0]  # Take the first match
                name = emp.get("name", "Unknown")
                dept = emp.get("department", "Unknown")
                role = emp.get("role", "Unknown")
                salary = emp.get("salary", 0)
                formatted_response = f"Employee Details:\nName: {name}\nDepartment: {dept}\nRole: {role}\nSalary: ${salary:,}"
            else:
                formatted_response = f"No employee found with name '{parameter}'."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee details query results"
            }
        
        elif query_type == "issues_by_employee":
            if data:
                issues_list = []
                for issue in data:
                    title = issue.get("title", "Unknown")
                    status = issue.get("status", "Unknown")
                    project_name = issue.get("project_name", "Unknown")
                    issue_str = f"{title} (Status: {status}, Project: {project_name})"
                    issues_list.append(issue_str)
                issues_formatted = "\n- ".join(issues_list)
                formatted_response = f"Issues faced by {parameter}:\n- {issues_formatted}"
            else:
                formatted_response = f"No issues found for {parameter}."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee issues query results"
            }
        
        elif query_type in ["employees_by_role", "all_employee_roles"]:
            if data:
                if query_type == "employees_by_role":
                    employees_list = []
                    for emp in data:
                        name = emp.get("name", "Unknown")
                        dept = emp.get("department", "Unknown")
                        salary = emp.get("salary", 0)
                        emp_str = f"{name}, {dept}, ${salary:,}"
                        employees_list.append(emp_str)
                    employees_formatted = "\n- ".join(employees_list)
                    formatted_response = f"Employees with role '{parameter}':\n- {employees_formatted}"
                else:  # all_employee_roles
                    roles = [item.get("role", "Unknown") for item in data]
                    roles_list = "\n- ".join(roles)
                    formatted_response = f"All employee roles in the organization:\n- {roles_list}"
            else:
                if query_type == "employees_by_role":
                    formatted_response = f"No employees found with role '{parameter}'."
                else:
                    formatted_response = "No employee roles found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Employee roles query results"
            }
        
        elif query_type in ["projects_by_department", "all_projects"]:
            if data:
                if query_type == "projects_by_department":
                    project_names = [proj.get("name", "Unknown") for proj in data]
                    projects_list = "\n- ".join(project_names)
                    formatted_response = f"Projects in {parameter} department:\n- {projects_list}"
                else:  # all_projects
                    projects_list = []
                    for proj in data:
                        name = proj.get("name", "Unknown")
                        dept = proj.get("department", "Unknown")
                        proj_str = f"{name} ({dept})"
                        projects_list.append(proj_str)
                    all_projects = "\n- ".join(projects_list)
                    formatted_response = f"All projects in the organization:\n- {all_projects}"
            else:
                if query_type == "projects_by_department":
                    formatted_response = f"No projects found in {parameter} department."
                else:
                    formatted_response = "No projects found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Project query results"
            }
        
        elif query_type in ["issues_by_status", "all_issues"]:
            if data:
                if query_type == "issues_by_status":
                    issues_list = []
                    for issue in data:
                        title = issue.get("title", "Unknown")
                        project_name = issue.get("project_name", "Unknown")
                        dept = issue.get("department", "Unknown")
                        issue_str = f"{title} (Project: {project_name}, Department: {dept})"
                        issues_list.append(issue_str)
                    issues_formatted = "\n- ".join(issues_list)
                    formatted_response = f"Issues with status '{parameter}':\n- {issues_formatted}"
                else:  # all_issues
                    issues_list = []
                    for issue in data:
                        title = issue.get("title", "Unknown")
                        status = issue.get("status", "Unknown")
                        project_name = issue.get("project_name", "Unknown")
                        dept = issue.get("department", "Unknown")
                        issue_str = f"{title} (Status: {status}, Project: {project_name}, Department: {dept})"
                        issues_list.append(issue_str)
                    all_issues = "\n- ".join(issues_list)
                    formatted_response = f"All issues in the organization:\n- {all_issues}"
            else:
                if query_type == "issues_by_status":
                    formatted_response = f"No issues found with status '{parameter}'."
                else:
                    formatted_response = "No issues found."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "Issue query results"
            }
        
        else:
            # Handle general queries with whatever data is available
            if data:
                # Try to determine the best way to present the data
                if all('name' in item for item in data):
                    # If all items have names, show as list
                    names = [item.get("name", "Unknown") for item in data]
                    names_list = "\n- ".join(names)
                    formatted_response = f"Here's what I found:\n- {names_list}"
                else:
                    # Otherwise, provide a general response
                    formatted_response = f"Found {len(data)} records."
            else:
                formatted_response = "No data found for your query."
            
            return {
                "query_type": query_type,
                "parameter": parameter,
                "data": data,
                "formatted_answer": formatted_response,
                "summary": "General query results"
            }