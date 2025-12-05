# Go Production CRUD API

A production-ready CRUD application written in Go, demonstrating clean architecture, dependency injection, and best practices.

## Architecture

The project follows a **Layered Architecture** (Clean Architecture):

-   **Handlers (`internal/handlers`)**: HTTP transport layer (Chi). Handles request parsing, validation, and response formatting.
-   **Service (`internal/service`)**: Business logic layer. Contains core domain logic and validation.
-   **Repository (`internal/repository`)**: Data access layer. Handles database interactions using GORM.
-   **Domain (`internal/domain`)**: Core business entities and interface definitions.

## Tech Stack

-   **Go 1.22+**
-   **Router**: [Chi](https://github.com/go-chi/chi) (Lightweight, idiomatic)
-   **Database**: SQLite (File-based for local/dev), GORM (ORM)
-   **Config**: [Viper](https://github.com/spf13/viper)
-   **Logging**: [Zap](https://github.com/uber-go/zap)
-   **Docs**: Swagger/OpenAPI

## Getting Started

### Prerequisites

-   Go 1.22+
-   Docker (optional)

### Setup

1.  Clone the repository.
2.  Copy `.env.example` to `.env`:
    ```sh
    cp .env.example .env
    ```
    (Or create it manually if on Windows)

### Running Locally

```sh
# Install dependencies
go mod download

# Run the application
go run cmd/api/main.go
```
The server will start on `http://localhost:8080`.

### Running with Docker

```sh
# Build and Run
docker-compose up --build
```

### Running Tests

```sh
go test ./... -v
```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health Check |
| `POST` | `/products` | Create a product |
| `GET` | `/products` | List products (Pagination: `?page=1&page_size=10`) |
| `GET` | `/products/{id}` | Get product by ID |
| `PUT` | `/products/{id}` | Update product |
| `DELETE` | `/products/{id}` | Delete product |

## Database

By default, the app uses **SQLite** stored in `data.db` (or `app.db` in Docker).

### Switching to PostgreSQL

1.  Update `internal/repository/db.go` to use `gorm.io/driver/postgres`.
2.  Update `NewSQLiteDB` to `NewPostgresDB` or generic `NewDB`.
3.  Change connection string/DSN in `internal/config`.

## Swagger Documentation

To generate Swagger docs (requires `swag` CLI):
```sh
swag init -g cmd/api/main.go
```
Then access at: `http://localhost:8080/swagger/index.html` (Requires adding `http-swagger` middleware, not enabled by default to keep deps low, but annotations are present).
