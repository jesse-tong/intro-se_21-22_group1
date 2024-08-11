FROM nikolaik/python-nodejs:python3.12-nodejs22-slim
WORKDIR /usr/src/app
COPY ./ /usr/src/app/

RUN mkdir data


RUN apt-get update && apt-get install -y netcat-traditional
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN npm install
RUN npm run build

ENTRYPOINT [ "./entrypoint.sh" ]