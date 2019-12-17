FROM python:3.7-alpine

RUN mkdir /app
ADD lottery.py /app/lottery.py

EXPOSE 1337

RUN chmod +x /app/lottery.py

ENTRYPOINT ["nc", "-lkvp", "1337", "-e", "python", "-u", "/app/lottery.py"]

