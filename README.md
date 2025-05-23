# Booklib API Works
The Booklib API is a backend service for managing audio books. It is built using the Flask framework and offers a set of RESTful endpoints for managing books, authors, categories, and users. Here’s a breakdown of the key components:

## Flask Application Factory:
* The create_app function sets up and configures the Flask application. This approach is known as the application factory pattern, which allows for easier testing and configuration.

## Environment Configuration:
* The application loads environment variables using dotenv, which allows configuration values to be set outside of the codebase.

## Database:
* SQLAlchemy is used as the ORM (Object-Relational Mapper) to interact with the database.
* Flask-Migrate is integrated for handling database migrations.

## JWT Authentication:
* The application uses Flask-JWT-Extended for handling JWT authentication, including token creation, validation, and revocation.
* Custom JWT callback functions are defined for various scenarios like token expiration, invalid tokens, and token revocation.

## Blueprints:
* The application is modularized using Flask blueprints. Each resource (books, authors, categories, users) has its own blueprint, which is registered with the main API object.
* This modular approach helps in organizing the codebase and making it more maintainable.

## Summary
The Booklib API is structured to be modular and maintainable, leveraging Flask blueprints, SQLAlchemy for ORM, Flask-Migrate for migrations, and Flask-JWT-Extended for authentication. By following the steps outlined above, you can add new endpoints that interact with the database seamlessly, ensuring the application remains organized and scalable.


Here's a help document for running the Booklib API in a local Docker container. This guide will walk you through setting up Docker, configuring environment variables, and starting the application.

---

# Docker Setup Guide

This guide will help you run the Booklib API in a local Docker container. Docker simplifies the setup process by creating an isolated environment for the application and its dependencies.

## Prerequisites

1. **Docker**: Ensure Docker is installed on your system. If not, you can download it from [Docker's official website](https://www.docker.com/get-started).

2. **Docker Compose (Optional)**: If your setup involves `docker-compose`, ensure it's installed. Most recent Docker Desktop versions include Docker Compose.

## Steps to Run Booklib API

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd booklib-api
```

### 2. Set Up Environment Variables

The application uses environment variables for configuration, including the database URL and JWT secret. Create a `.env` file in the root directory, or modify `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with appropriate values. Key variables include:
- `DATABASE_URL`: Specify your database URL (if using PostgreSQL, a URL like `postgresql://user:password@db:5432/booklib`).
- `JWT_SECRET_KEY`: Define a secret key for JWT token encryption.

### 3. Build and Run Docker Container

The repository includes a `Dockerfile` and potentially a `docker-compose.yml` file for simplified container management.

#### Using `Dockerfile` Only

To build and run the container manually:

1. **Build the Docker Image**:

    ```bash
    docker build -t booklib-api .
    ```

2. **Run the Docker Container**:

    ```bash
    docker run -d -p 5000:5000 --env-file .env booklib-api
    ```

   This command maps port `5000` on your machine to port `5000` in the container, where the Flask API will be running.

#### Using `docker-compose`

If a `docker-compose.yml` file is provided, you can use it to simplify the setup, especially if there are multiple services (e.g., database, API) involved.

1. **Run Docker Compose**:

    ```bash
    docker-compose up -d
    ```

    This will start all defined services in the `docker-compose.yml` file. 

### 4. Access the Application

Once the container is running, access the Booklib API at `http://localhost:5000`.

### 5. Stopping the Application

To stop the application, you can use:

- **For `docker-compose`**:
  
  ```bash
  docker-compose down
  ```

- **For Docker Run**:

  ```bash
  docker ps  # Find the container ID
  docker stop <container-id>
  ```

---

## Troubleshooting

- **Port Conflicts**: If port `5000` is in use, you can map another port by changing `-p 5000:5000` to `-p <your-port>:5000`.
- **Environment Variables**: Ensure `.env` is properly configured, especially `DATABASE_URL` and `JWT_SECRET_KEY`.
- **Docker Permissions**: If you encounter permission issues, try running Docker commands with `sudo`, or check Docker permissions on your system.

This should help you set up and run the Booklib API locally with Docker. Let me know if you have any questions!
