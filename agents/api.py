from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.planner_agent import PlannerAgent
from agents.response_agent import ResponseAgent

app = FastAPI()

# Serve static files but prioritize API routes
app.mount("/static", StaticFiles(directory="static"), name="static")

planner = PlannerAgent()
# Get the MCP interface from the planner agent
mcp_interface = planner.get_mcp_interface()
responder = ResponseAgent()

class Query(BaseModel):
    question: str

@app.post("/query")
def query_db(q: Query):
    # Agent 1: LLM Planner - analyze the query
    query_analysis = planner.analyze_query(q.question)
    
    query_type = query_analysis["type"]
    parameter = query_analysis["parameter"]
    
    # Agent 2: Execute appropriate database query through MCP framework based on semantic analysis
    result = []
    
    # Map semantic query types to appropriate MCP interface methods
    if query_type in ["employee_by_department", "employees_by_department"]:
        result = mcp_interface.execute_structured_query("employees_by_department", {"department": parameter})
    elif query_type == "all_employees":
        result = mcp_interface.execute_structured_query("all_employees", {})
    elif query_type == "count_employees":
        # For count queries, get stats from MCP interface
        stats = mcp_interface.get_db_stats()
        result = [{"count": stats['employee_count']}]
    elif query_type == "employee_names_with_roles":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        result = [{"name": emp["name"], "role": emp["role"]} for emp in all_employees]
    elif query_type == "employee_names_with_projects":
        # Get employees and join with projects via department
        employees = mcp_interface.execute_structured_query("all_employees", {})
        projects = mcp_interface.execute_structured_query("all_projects", {})
        result = []
        for emp in employees:
            emp_dept = emp["department"]
            emp_projects = [proj for proj in projects if proj["department"] == emp_dept]
            if emp_projects:
                for proj in emp_projects:
                    result.append({
                        "name": emp["name"],
                        "role": emp["role"],
                        "project": proj["name"]
                    })
            else:
                result.append({
                    "name": emp["name"],
                    "role": emp["role"],
                    "project": "No specific project assigned"
                })
    elif query_type == "employee_names_with_salaries":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        result = [{"name": emp["name"], "salary": emp["salary"]} for emp in all_employees]
    elif query_type == "all_employee_names":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        result = [{"name": emp["name"]} for emp in all_employees]
    elif query_type == "all_employee_roles":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        roles = list(set(emp["role"] for emp in all_employees))
        result = [{"role": role} for role in roles]
    elif query_type == "all_employee_salaries":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        result = [{"name": emp["name"], "salary": emp["salary"]} for emp in all_employees]
    elif query_type == "all_employee_departments":
        all_employees = mcp_interface.execute_structured_query("all_employees", {})
        depts = list(set(emp["department"] for emp in all_employees))
        result = [{"department": dept} for dept in depts]
    elif query_type == "all_projects":
        result = mcp_interface.execute_structured_query("all_projects", {})
    elif query_type == "all_issues":
        result = mcp_interface.execute_structured_query("all_issues", {})
    elif query_type == "employees_by_role":
        result = mcp_interface.execute_structured_query("employees_by_role", {"role": parameter})
    elif query_type == "employee_by_name":
        result = mcp_interface.execute_structured_query("employee_by_name", {"name": parameter})
    elif query_type == "issues_by_employee":
        result = mcp_interface.execute_structured_query("issues_by_employee", {"name": parameter})
    elif query_type == "projects_by_department":
        result = mcp_interface.execute_structured_query("projects_by_department", {"department": parameter})
    elif query_type == "issues_by_status":
        result = mcp_interface.execute_structured_query("issues_by_status", {"status": parameter})
    elif query_type in ["employee_by_name", "employee_details"]:
        result = mcp_interface.execute_structured_query("employee_by_name", {"name": parameter})
    elif query_type == "unknown" or query_type == "general_query":
        # For unknown or general queries
        result = mcp_interface.execute_structured_query("all_employees", {})
    else:
        # Default fallback for any other unrecognized query types
        result = mcp_interface.execute_structured_query("all_employees", {})
    
    # Agent 3: Response Agent
    return responder.format(query_analysis, result)

# Catch-all route for frontend (must be defined AFTER API routes)
@app.get("/{full_path:path}")
def serve_frontend(full_path: str = ""):
    from fastapi.responses import FileResponse
    import os
    
    # If accessing root or html files, serve index.html
    if full_path == "" or full_path == "/" or full_path.endswith(".html"):
        return FileResponse("static/index.html")
    # For other static assets (css, js, images), let the static mount handle them
    elif os.path.exists(f"static/{full_path}"):
        return FileResponse(f"static/{full_path}")
    else:
        return FileResponse("static/index.html")  # Fallback to index.html

@app.on_event("shutdown")
def shutdown_event():
    """Close the MCP database connection when shutting down"""
    mcp_interface.close()