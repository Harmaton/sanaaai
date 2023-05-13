FROM python:3.8-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

# Set environment variables
ENV FLASK_APP = app.py
ENV FLASK_DEBUG = production

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
