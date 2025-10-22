FROM python:3.13.7-alpine

WORKDIR /home/app

COPY dep.txt .

RUN pip install -r dep.txt

COPY . .

EXPOSE 8000

CMD [ "fastapi","run" ]