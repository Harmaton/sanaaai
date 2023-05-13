FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

# Set environment variables
ENV FLASK_APP = app.py
ENV FLASK_DEBUG = production

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
