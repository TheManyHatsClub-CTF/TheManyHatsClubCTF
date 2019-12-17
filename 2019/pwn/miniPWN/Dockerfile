FROM alpine:latest

RUN mkdir /app
COPY pwn /app/
COPY flag.txt /app/
RUN chmod +x /app/pwn
RUN adduser imth --disabled-password -s $(which nologin)
EXPOSE 1337
USER imth
WORKDIR /app/
ENTRYPOINT ["nc", "-lkvp", "1337", "-e", "/app/pwn"]
