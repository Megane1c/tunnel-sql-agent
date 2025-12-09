import requests
import json
from typing import Optional, Dict, Any

from agno.tools import Toolkit
from agno.tools.function import ToolResult

class RemotePostgresTools(Toolkit):
    def __init__(
        self,
        base_url: str,
    ):
        super().__init__(name="remote_postgres_tools")
        self.base_url = base_url.rstrip("/")
        self.register(self.get_schema)
        self.register(self.run_query)

    def get_schema(self) -> ToolResult:
        """
        Retrieves the schema of the remote database.
        
        Returns:
            str: JSON string representation of the schema.
        """
        try:
            response = requests.get(f"{self.base_url}/schema", timeout=10)
            response.raise_for_status()
            return ToolResult(content=json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            return ToolResult(content=json.dumps({"error": f"Error fetching schema: {e}"}, indent=2))

    def run_query(self, query: str) -> ToolResult:
        """
        Executes a SQL query on the remote database.
        
        Args:
            query (str): The SQL query to execute. MAKE SURE TO ONLY RUN SELECT STATEMENTS.
            
        Returns:
            str: The results of the query or an error message.
        """
        try:
            response = requests.post(
                f"{self.base_url}/query", 
                json={"query": query},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if "results" in data:
                return ToolResult(content=json.dumps(data["results"], indent=2, ensure_ascii=False))
            return ToolResult(content=json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            # Try to get error details from response
            try:
                error_detail = response.json().get("detail", str(e))
                return ToolResult(content=json.dumps({"error": f"Error executing query: {error_detail}"}, indent=2))
            except:
                return ToolResult(content=json.dumps({"error": f"Error executing query: {e}"}, indent=2))
