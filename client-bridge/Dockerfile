FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Chisel
ARG CHISEL_VERSION=1.11.3
RUN curl -sSL https://github.com/jpillora/chisel/releases/download/v${CHISEL_VERSION}/chisel_${CHISEL_VERSION}_linux_amd64.gz | gzip -d > /usr/local/bin/chisel && \
    chmod +x /usr/local/bin/chisel

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App
COPY main.py .
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
