FROM ubuntu

RUN apt-get update && apt-get install -y python-pip && apt-get install -y nodejs && apt-get install -y npm

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY package.json /app
COPY requirements.txt /app

# Install any needed packages specified in package.json and requirements.txt
RUN npm install
RUN pip install -r requirements.txt

# Bundle app source
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

CMD [ "npm", "start" ]