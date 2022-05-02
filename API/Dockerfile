FROM golang:1.17

# Create a new directory for our code
RUN mkdir /app
ADD . /app
WORKDIR /app

# Get go.mod and main.go files
ADD ./go.mod /
ADD ./main.go /

# Download dependencies and build - put our executable in its own folder for gitignore
RUN CGO_ENABLED=0 GOOS=linux go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o ./bin/main

# Ports we want to use for this
EXPOSE 8080 8080

# Give permissions to main and run
RUN chmod +x ./bin/main

CMD ./bin/main
