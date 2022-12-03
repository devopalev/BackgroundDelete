
FROM python:3.10.8-alpine

COPY requirements.txt .

RUN apk update ; apk add make cmake automake gcc g++ subversion python3-dev gfortran openblas lapack onnxruntime
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install --user -r requirements.txt



COPY ./source/run.py /app/
WORKDIR /app/
CMD ["python", "-u", "./run.py"]

EXPOSE 8080
