# Use a lightweight, official Python base image
FROM python:3.11-slim

# Set the working directory inside the virtual environment
WORKDIR /app

# Copy the core script directly into the container filesystem
COPY main.py .

# Configure system variables to ensure pure UTF-8 formatting output
ENV PYTHONIOENCODING=utf-8

# Run the virtual OS overdrive simulator immediately on startup
CMD ["python", "-u", "main.py"]
