
FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy source code
COPY . .

# Expose running ports:
ENV PORT=5000 

EXPOSE $PORT

#run via gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT main.server.app:app"]
