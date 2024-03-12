# Use the official Python 3.11 image as base image
FROM python:3.11-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl gdal-bin libgdal-dev g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

RUN pip3 install --upgrade pip --no-cache-dir \
    && pip3 install -r streamlit-prettymapp/requirements.txt --no-cache-dir

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run your application
ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]