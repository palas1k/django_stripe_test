FROM python:3.10-alpine
COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
COPY . /app
WORKDIR /app/core
EXPOSE 8000