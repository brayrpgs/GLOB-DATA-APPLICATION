FROM python:3.13.7-alpine

RUN mkdir -p /home/app

WORKDIR /home/app

COPY . .

RUN python -m venv venv

RUN pip install -r dep.txt

EXPOSE 8000

CMD [ "fastapi","run" ]