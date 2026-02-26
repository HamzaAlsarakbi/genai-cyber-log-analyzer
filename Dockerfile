# Use a lightweight, secure Python base image
FROM python:3.11-slim

# Create a non-root user for security (Bank of Canada loves this)
RUN useradd --create-home appuser

# Set the working directory
WORKDIR /app

# Copy requirements and install them securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and dummy log file
COPY main.py .
COPY server_logs.txt .

# Change ownership of the files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Run the GenAI analyzer
ENTRYPOINT ["python", "main.py"]

# Provide default arguments just in case none are passed
CMD ["-f", "server_logs.txt"]