FROM python:3-slim-buster

WORKDIR /usr/src/deposite_calc

COPY ./requirements.txt .
COPY ./app ./app
COPY ./tests ./tests

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "flask",  "--app", ".", "run"]
