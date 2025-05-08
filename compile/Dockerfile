# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc valgrind htop
RUN pip install uv


# Make port 80 available to the world outside this container
EXPOSE 80



# add a new user
RUN useradd -ms /bin/bash badbot


# Set the working directory in the container
WORKDIR /app




# Copy the current directory contents into the container at /app
COPY . /app
RUN mkdir /run_logs
RUN mkdir /jobs
RUN chown -R badbot:badbot /app \
    && chmod -R o-w /app \
    && chmod -R o+rx /app \
    && chmod -R o+rx /app
USER badbot
RUN sed -ie "s/\r//g" ./*.sh



RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt

# add permissions




# Run hello.py when the container launches



CMD ["uv","run", "worker.py"]
