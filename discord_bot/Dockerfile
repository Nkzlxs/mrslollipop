FROM python:3.9.2-buster

WORKDIR /bot_dir

COPY *.py ./
COPY requirements.txt .

# Credentials file
COPY credential.json .


RUN pip install -r requirements.txt



CMD python3 entrypoint.py "python3 bot.py --main"
