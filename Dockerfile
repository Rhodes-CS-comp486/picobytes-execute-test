# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc
RUN pip install uv
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt


# Make port 80 available to the world outside this container
EXPOSE 80


RUN sed -ie "s/\r//g" ./compile/*.sh

WORKDIR ./api
# Run hello.py when the container launches

CMD ["uv","run", "server_api.py"]
