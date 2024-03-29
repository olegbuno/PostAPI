FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Copy the requirements file to the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the local app directory to the container
COPY ./app /app/app
