# =======================
# 1️⃣ Build stage
# =======================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

# Install dependencies in a temp folder to copy later
RUN pip install --user -r requirements.txt

# =======================
# 2️⃣ Final stage
# =======================
FROM python:3.12-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy project files
COPY . .

# Expose FastAPI port (inside container)
EXPOSE 8000

# Default command
CMD ["uvicorn", "product.main:app", "--host", "0.0.0.0", "--port", "8000"]
