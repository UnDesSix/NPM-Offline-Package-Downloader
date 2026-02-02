FROM node:22.17.1

WORKDIR /home/node/app

COPY ./script_dependencies.py /home/node/app/script_dependencies.py
COPY ./package.json /home/node/app/package.json

RUN apt-get update && \
    apt-get install -y python3-venv && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir tqdm

ENV PATH="/opt/venv/bin:$PATH"

RUN npm install --package-lock-only --legacy-peer-deps

CMD ["python3", "script_dependencies.py"]
