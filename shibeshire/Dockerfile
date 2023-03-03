FROM python:3.8.13-alpine3.14
WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache git
RUN pip install -r requirements.txt
CMD python bot.py
