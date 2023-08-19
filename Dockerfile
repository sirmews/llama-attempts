# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /app

# Update system packages and install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install the required packages from requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# Run the application
CMD ["bash"]
