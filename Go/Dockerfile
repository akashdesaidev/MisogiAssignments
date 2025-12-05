# Build Stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=1 GOOS=linux go build -o main ./cmd/api

# Run Stage
FROM alpine:latest

WORKDIR /app

# SQLite requires CGO, so we need runtime libraries. Alpine is usually fine but let's be safe.
RUN apk add --no-cache sqlite-libs

COPY --from=builder /app/main .
COPY --from=builder /app/.env.example .env

# Expose port
EXPOSE 8080

# Environment variables
ENV SERVER_PORT=8080
ENV DATABASE_FILE=/data/app.db

# Create volume dir
RUN mkdir /data

CMD ["./main"]
