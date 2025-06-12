# ---------- FedMCP Foundry connector ----------
# Lightweight image that bundles the standalone connector code.
# Build with:
#   docker build -t fedmcp/foundry-connector ./foundry_conn
# Run with the expected env vars:
#   docker run -e FOUNDRY_URL=… -e FOUNDRY_TOKEN=… fedmcp/foundry-connector

FROM python:3.11-slim

# Install OS packages required by cryptography / jwcrypto wheels
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends build-essential libssl-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non‑root user for better security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# ---- Python deps ----
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Connector source ----
COPY connector.py .
COPY tool.schema.json .

# Default entrypoint simply prints help; the parent
# process (agent runner) can override the CMD to `python connector.py`
CMD ["python", "connector.py", "--help"]
