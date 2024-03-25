# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.7-alpine
WORKDIR /app 
COPY . /app
RUN pip3 install -r requirements.txt --no-cache-dir
ENTRYPOINT ["python3"] 
CMD ["client.py"]