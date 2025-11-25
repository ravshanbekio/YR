FROM python:3.13-slim

# Set the working directory to the top-level app folder inside the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY all contents of local ./backend/app (where main.py is) into the container's WORKDIR (/app)
# This places main.py at /app/main.py
COPY ./backend/app/ .

COPY .env .

EXPOSE 8000
# CMD path: Look for main.py inside the current working directory (/app).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]