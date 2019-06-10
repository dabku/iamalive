FROM python:3.6-alpine3.8

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY iamalive/ iamalive/
COPY setup.py .

RUN [ "python", "setup.py", "install" ]

WORKDIR /usr/src/app/iamalive

CMD [ "python", "run_server.py", "demo" ]

EXPOSE 5000

