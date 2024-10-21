FROM python:3.10.12-slim-bullseye
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

# CMD ["python", "start.py"]
CMD ["sh", "-c", "git log -1 --pretty=format:'%H;%h;%cI;%ce;%cn' > git_log.txt && python start.py"]