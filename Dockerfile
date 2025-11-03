FROM node:20.12.2

WORKDIR /home/node/app

COPY ./script_dependencies.py /home/node/app/script_dependencies.py
COPY ./package.json /home/node/app/package.json

RUN npm install --package-lock-only --legacy-peer-deps

CMD ["python3", "script_dependencies.py"]
