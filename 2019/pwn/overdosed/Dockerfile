FROM alpine:latest

RUN apk add libc6-compat
RUN mkdir /app
COPY overdosed /app/
COPY flag.txt /app/
RUN chmod +x /app/overdosed
RUN adduser QHpix --disabled-password -s $(which nologin)
EXPOSE 1337
USER QHpix
WORKDIR /app/
ENTRYPOINT ["nc", "-lkvp", "1337", "-e", "/app/overdosed"]