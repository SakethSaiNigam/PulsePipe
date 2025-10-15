FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

# Default command spins up API
CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8000"]
