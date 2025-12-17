from agno.agent import Agent
from agno.models.ollama import Ollama
from tools import RemotePostgresTools

# Configuration, coming from the server
CLIENT_TUNNEL_URL = "http://localhost:10001"

print(f"Initializing Agent for client at {CLIENT_TUNNEL_URL}...")

# Initialize Custom Remote Tool
remote_tools = RemotePostgresTools(base_url=CLIENT_TUNNEL_URL)

# Initialize Agent
agent = Agent(
    name="AaaS SQL Assistant",
    model=Ollama(id="gpt-oss-safeguard:120b", host="http://localhost:11434", 
                      options={"temperature": 0.3}),
    tools=[remote_tools],
    instructions="""You are a SQL expert assisting a client with their remote database.
    1. Always start by inspecting the schema using `get_schema()` if you don't know the table structure.
    2. Convert natural language queries to SQL and use `run_query()`.
    3. The database is PostgreSQL.
    """,
    markdown=True,
)

if __name__ == "__main__":
    print("Starting interactive mode...")
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            agent.print_response(user_input)
        except KeyboardInterrupt:
            break
