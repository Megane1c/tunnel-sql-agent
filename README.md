# Tunnel SQL Agent POC

This project demonstrates a secure, tunneled connection between an AI Agent and a private database using [Chisel](https://github.com/jpillora/chisel). It includes a "Bridge" container that acts as a secure gateway for the database, allowing the AI to query it without exposing the database to the public internet.

The sample database used for this POC is [Chinook](https://github.com/lerocha/chinook-database), representing a digital media store.

## Architecture

```
Client (remote network)               Server (agent host)
┌───────────────────────┐            ┌──────────────────┐
│  PostgreSQL (local)   │            │  AI Agent        │
│  API Wrapper          │◄──────────►│                  │
│  Chisel Client        │  (tunnel)  │  Chisel Server   │
└───────────────────────┘            └──────────────────┘
```

-   **Server**: Runs the Chisel Server (Reverse Proxy) and the AI Agent.
-   **Client Bridge**: A Docker container running:
    -   **Chinook Database**: PostgreSQL instance with sample data.
    -   **API Wrapper**: A lightweight API around the DB.
    -   **Chisel Client**: Connects out to the Server, creating a reverse tunnel.

## Prerequisites

-   Docker & Docker Compose
-   `wget` (to download Chisel)
-   Python 3.10+ (for the Agent)

## Quick Start Guide

### 1. Setup the Tunnel Server

First, download the Chisel binary. We'll use this to run the tunnel server.

```bash
# Download Chisel (Linux amd64)
wget https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_amd64.gz

# Unzip and make executable
gzip -d chisel_1.11.3_linux_amd64.gz
mv chisel_1.11.3_linux_amd64 chisel
chmod +x chisel
```

Now, start the server. This listens for incoming connections from the client bridge.

```bash
# Run in a dedicated terminal
./chisel server --authfile users.json --reverse --port 9090
```
-   `--authfile users.json`: Uses the provided `users.json` for client authentication (`client_1:pass_123`).
-   `--reverse`: Allows clients to open reverse ports (exposing their local API to us).
-   `--port 9090`: The port the server listens on.

### 2. Start the Client Bridge (Client Side)

The client runs a single Docker Compose stack that includes the database and the tunnel.

Open a **new terminal** and run:

```bash
cd client-bridge

# Start the compose
docker compose up
# Note: We are NOT using -d so you can see the connection logs
```

*Wait until you see `client: Connected` in the logs.*

### 3. Run the AI Agent

Now that the tunnel is established, the AI Agent can talk to the remote database as if it were local.

Open a **third terminal** and run:

```bash
# Install dependencies
pip install agno ollama

# Run the Agent
python run_agent.py
```

### 4. Sample Questions

Try asking the agent these questions to explore the Chinook database:

1.  What is the database all about?
2.  What is the total revenue for each country?
3.  Which salesperson generated the highest revenue?


## Acknowledgements

-   **[Agno](https://github.com/agno-agi/agno)**: For the powerful Agentic AI framework.
-   **[Chisel](https://github.com/jpillora/chisel)**: For the fast, secure TCP tunnel over HTTP.
-   **[Chinook Database](https://github.com/lerocha/chinook-database)**: For the comprehensive sample database schema and data.
