FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make run.sh executable
RUN chmod +x /app/run.sh

# Run entrypoint script
ENTRYPOINT ["/app/run.sh"] 