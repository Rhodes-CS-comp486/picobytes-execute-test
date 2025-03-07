# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y gcc
RUN pip install uv


# Make port 80 available to the world outside this container
EXPOSE 80



# add a new user
RUN useradd -ms /bin/bash badbot


# Set the working directory in the container
WORKDIR /usr/app




# Copy the current directory contents into the container at /app
COPY . /usr/app


RUN sed -ie "s/\r//g" ./compile/*.sh



RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt

# ad permissions
RUN chown -R badbot:badbot /usr/app && chmod -R o-rwx /usr && chmod -R o+rx /usr/app

# switch to the new user
USER badbot





WORKDIR /usr/app/api

# Run hello.py when the container launches

CMD ["uv","run", "server_api.py"]
