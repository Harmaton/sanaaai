# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

# Set environment variables
ENV FLASK_APP = app.py
ENV FLASK_DEBUG = production

# Expose port 8080 for gunicorn
EXPOSE 8080

# Run the command to start the gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
