# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system and Python dependencies
RUN apt-get update && \
    apt-get install -y build-essential openslide-tools libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Jupyter Lab
RUN pip install jupyterlab

# Copy the entire genomic_plip_model directory contents into the container at /app
COPY ./ /app/

# Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it for security
RUN adduser --disabled-password --gecos '' myuser
USER myuser

EXPOSE 8888

# Run process_tiles.py when the container launches
CMD ["python", "./process_tiles.py"]
