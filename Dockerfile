#set of commands the user can make when setting up the project
FROM python:3

#ensuring that the python output direcrtly goes to the terminal without buffer
ENV PYTHONUNBUFFERED=1

# The absolute or relative path to use as the working directory. Will be created if it does not exist.
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

#copy the . (current working directory) into  /code/ 
# COPY . /code/  