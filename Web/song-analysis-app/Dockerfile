FROM node:alpine

# add source code to the image
WORKDIR /app

# copy list of dependencies
COPY package.json ./

# install dependencies
RUN npm install

# copy all files in the application to the image
COPY . .

# ports to use
EXPOSE 3000

# start up application
CMD ["npm", "start"]
