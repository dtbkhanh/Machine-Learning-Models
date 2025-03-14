FROM python:3.6-slim

WORKDIR /usr/src/ui

COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

COPY ["run.py", "./"]
COPY app /usr/src/ui/app

EXPOSE 80
# Run app.py when the container launches


CMD python run.py