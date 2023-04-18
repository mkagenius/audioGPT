# Use an official Python base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY src/ .

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Start Gunicorn to run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app", "-t", "1200"]
