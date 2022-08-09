# The Dockerfile is a text document that contains the commands 
# used to assemble the image. The FROM command specifies the 
# base container image on which the new image will be built. 
# The tag specifies the interpreter version
FROM python:3.8.13

# Execute an arbitrary command in the context of the container.
RUN apt-get update

# The WORKDIR command sets a default directory where the 
# application is going to be installed.
WORKDIR /code

# The ENV command sets environment variables inside the 
# container required to use the flask command.
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# The COPY command transfers files from your machine to the 
# container file system and installs the Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# The EXPOSE command configures the port that this container 
# will be using for its server.
EXPOSE 5000

# Copy the current directory . in the project to the 
# workdir . in the image.
COPY . .

# Set the default command for the container to flask run
CMD ["flask", "run"]