FROM python:3.10.8-buster

COPY requirements.txt .

RUN pip3 install --upgrade pip ; pip3 install --user -r requirements.txt
ENV MODEL="u2netp"

COPY . /app/
WORKDIR /app/source

HEALTHCHECK --start-period=10s --interval=2m --timeout=10s CMD curl --fail http://localhost:8080/healthcheck || exit 1

EXPOSE 8080

CMD ["python", "-u", "./run.py"]