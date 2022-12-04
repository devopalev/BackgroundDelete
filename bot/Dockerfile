
FROM python:3.10.8-alpine

COPY requirements.txt .
RUN pip3 install --upgrade pip ; pip3 install --user -r requirements.txt

ENV TG_BOT_TOKEN="YOUR_TOKEN"
ENV URL_MICROSERVICE_EDIT_IMAGES="http://YOUR_SERVICE"

COPY . /app/
WORKDIR /app/source
CMD ["python", "-u", "./run.py"]

EXPOSE 8080
