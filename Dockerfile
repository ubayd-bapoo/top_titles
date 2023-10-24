# Use the official openjdk image
FROM openjdk:11-jre-slim

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements.txt file first and install Python dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the local script and requirements.txt to the container
COPY . /app/

EXPOSE 8000

# Run the script when the container starts
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]