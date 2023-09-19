FROM python:latest

# # Install dependencies
# ADD resolv.conf /etc/resolv.conf
RUN apt-get update \
    && apt-get upgrade \
    && apt-get install postgresql-client -y


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
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

