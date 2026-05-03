# ===============================
# Base Image
# ===============================
FROM python:3.9-slim

# ===============================
# Set Working Directory
# ===============================
WORKDIR /app

# ===============================
# Copy Project Files
# ===============================
COPY . .

# ===============================
# Install Dependencies
# ===============================
# CHANGED: Use requirement-docker.txt which has both backend and frontend dependencies
RUN pip install --no-cache-dir -r requirement-docker.txt

# ===============================
# Expose Ports
# ===============================
EXPOSE 8000
EXPOSE 8501

# ===============================
# Run API + Streamlit Together
# ===============================
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]