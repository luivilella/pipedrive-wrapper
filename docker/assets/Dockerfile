FROM node:9

EXPOSE 3000

WORKDIR /deploy

ADD . /deploy

RUN yarn install --allow-root

CMD [ "yarn", "run", "build:prod" ]
