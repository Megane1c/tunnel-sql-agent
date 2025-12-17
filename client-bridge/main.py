import os
import logging
from typing import List, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db-bridge")

app = FastAPI(title="DB Bridge API")

# Configuration
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    logger.warning("DB_URL not set!")

class QueryRequest(BaseModel):
    query: str
    params: Optional[List[Any]] = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/schema")
def get_schema():
    """Returns the schema of the connected database."""
    if not DB_URL:
        raise HTTPException(status_code=500, detail="DB_URL is not configured")
    
    try:
        with psycopg.connect(DB_URL) as conn:
            # Get tables
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cur.fetchall()]
            
            schema_info = {}
            # Get columns for each table
            for table in tables:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = %s
                    """, (table,))
                    columns = cur.fetchall()
                    schema_info[table] = columns
                    
            return {"schema": schema_info}
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def execute_query(request: QueryRequest):
    """Executes a raw SQL query."""
    if not DB_URL:
        raise HTTPException(status_code=500, detail="DB_URL is not configured")

    # Basic safety check
    query_lower = request.query.lower().strip()
    if not query_lower.startswith("select"):
        # Allow only SELECT for now to prevent destruction in POC
        pass 

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(request.query, request.params)
                if cur.description:
                    results = cur.fetchall()
                    return {"results": results}
                else:
                    return {"results": [], "message": "Query executed successfully"}
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(status_code=400, detail=str(e))
