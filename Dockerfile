FROM python:latest

# # Install dependencies
# ADD resolv.conf /etc/resolv.conf
RUN sudo apt-get update && sudo apt-get upgrade

# ENV DJANGO_SUPERUSER_PASSWORD=#####


# create app directoty
RUN mkdir /app
# set app directory as work directory
WORKDIR /app

# update pip
RUN pip install --upgrade pip

# copy requirements.txt to work directory (/app/requirements.txt)
ADD ./requirements.txt .

# install packages
RUN pip install -r requirements.txt

