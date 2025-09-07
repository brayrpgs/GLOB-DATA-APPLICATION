FROM python:3.13.7

RUN mkdir -p /home/app

WORKDIR /home/app

COPY . .

RUN pip install -r dep.txt

EXPOSE 8000

CMD [ "fastapi","run" ]