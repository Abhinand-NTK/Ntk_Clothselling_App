FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update -q \
    && apt-get install -yq libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run your application
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
