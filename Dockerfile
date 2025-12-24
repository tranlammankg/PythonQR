FROM python:3.11-slim

WORKDIR /app

# Install build dependencies (if needed) and clean up
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8989

# Run with gunicorn for production-like server
CMD ["gunicorn", "-b", "0.0.0.0:8989", "QRcode:app"]
