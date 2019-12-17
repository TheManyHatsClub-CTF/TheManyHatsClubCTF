FROM python:3.6.8-alpine
LABEL image for a very simple flask application
WORKDIR /app
COPY . .
EXPOSE 80
RUN ["pip3", "install", "pipenv"]
RUN ["pipenv", "install"]
RUN pip3 install -r requirements.txt
CMD pipenv run python3 app.py
