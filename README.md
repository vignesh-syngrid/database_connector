# MCP AI-Powered Database Search System

## Overview

This project demonstrates an AI-powered database query system that uses LLM (Large Language Model) technology to understand natural language queries and translate them into structured database operations through the Model Context Protocol (MCP).

## Architecture

### Core Components

1. **Planner Agent** - Uses Google's FLAN-T5 transformer model to analyze natural language queries semantically
2. **Response Agent** - Formats database results into human-readable responses
3. **MCP Framework** - Secure bridge between LLM and database operations
4. **Frontend Interface** - User-friendly web interface for interacting with the system

### MCP Framework as Connector Layer

The Model Context Protocol (MCP) acts as a secure intermediary between the LLM and the database:

```
Natural Language Query → Planner Agent (LLM) → MCP Framework → Database → MCP Framework → Response Agent → Formatted Response
```

#### Key Features of MCP:
- **Secure Access**: Prevents direct database access from LLM, avoiding credential exposure
- **Structured Queries**: Translates LLM interpretations into safe, parameterized database operations
- **Abstraction Layer**: Provides a standardized interface for LLM-database interaction
- **Safety**: Eliminates SQL injection risks through pre-defined query types

## How It Works

### 1. Query Processing Flow
1. User submits natural language query (e.g., "Show all employees")
2. Planner Agent uses LLM to semantically analyze the query
3. MCP Framework translates the interpreted intent into structured database operations
4. Database executes the safe, parameterized query
5. Results are formatted by the Response Agent
6. User receives human-readable response

### 2. Semantic Search Capabilities
- The system understands equivalent queries like:
  - "Show all employees" ≡ "Give me employee names"
  - Uses transformer-based semantic analysis rather than keyword matching
- Handles variations in phrasing and terminology

### 3. MCP Query Types
The MCP framework supports various query types:
- `all_employees`: Fetch all employee records
- `employees_by_department`: Fetch employees by department
- `issues_by_employee`: Fetch issues related to an employee's department
- `count_employees`: Get employee count
- `all_projects`: Fetch all projects
- `all_issues`: Fetch all issues

## Configuration

### Prerequisites
- Python 3.8+
- Pip

### Installation
```bash
git clone <repository-url>
cd mcp_dummy
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Initialize Database
```bash
python database/init_db.py
```

### Running the Application
```bash
uvicorn agents.api:app --host 127.0.0.1 --port 8004
```

The application will be accessible at `http://127.0.0.1:8004`

## MCP Framework Deep Dive

### Security Model
The MCP framework implements a zero-trust model:
- LLM never sees database credentials
- All queries are pre-approved and parameterized
- Direct SQL injection is impossible
- Access is limited to predefined operations

## Technical Stack
- **Backend**: FastAPI, Uvicorn
- **LLM**: Transformers (FLAN-T5 model)
- **Database**: SQLite with MCP abstraction
- **Frontend**: HTML/CSS/JavaScript
- **Framework**: Custom MCP (Model Context Protocol)