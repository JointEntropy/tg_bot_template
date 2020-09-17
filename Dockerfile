# set base image (host OS)
FROM python:3.8


# copy the dependencies file to the working directory
#COPY requirements.in .
COPY bot_template/requirements.txt .
COPY config.json .

# install dependencies
RUN pip install --upgrade pip
#RUN pip freeze  requirements.in > requirements.txt
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY bot_template/src /src/.
#WORKDIR /src

# command to run on container start
#CMD [ "ls", "./src/" ]
#CMD [ "python", "/src/db/entities.py"]
CMD [ "python", "/src/runner.py" ]