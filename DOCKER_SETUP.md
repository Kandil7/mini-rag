# Docker Setup Guide for Mini RAG Application

## Prerequisites

Before running the application with Docker, ensure you have:

1. **Docker Desktop** installed and running on your machine
2. **Docker Compose** (usually comes with Docker Desktop)

## Setup Instructions

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials



```bash
$ cd docker
$ sudo docker compose up -d
```


### 1. Start Docker Desktop
Make sure Docker Desktop is running before proceeding with the following steps.

### 2. Build and Start Services

Run the following command from the project root directory:

```bash
docker compose -f docker/docker-compose.yml up -d
```

This will:
- Build the application container
- Start MongoDB service
- Start the Mini RAG application
- Run services in detached mode

### 3. Check Service Status

To verify that services are running:

```bash
docker compose -f docker/docker-compose.yml ps
```

### 4. View Logs

To view logs for debugging:

```bash
docker compose -f docker/docker-compose.yml logs -f
```

### 5. Access the Application

Once services are running, you can access:
- The Mini RAG API at: `http://localhost:8000`
- MongoDB is available internally at: `mongodb://mongodb:27017`

### 6. Stop Services

To stop the services:

```bash
docker compose -f docker/docker-compose.yml down
```

## Troubleshooting

### Common Issues:

1. **Docker daemon not running**: Make sure Docker Desktop is started
2. **Port already in use**: Check if ports 8000 or 27017 are already in use
3. **Permission errors**: Ensure you have proper permissions to run Docker

### Building Individual Components:

If you need to rebuild just the application:

```bash
docker build -t mini-rag-app .
```

Or rebuild just the MongoDB container:

```bash
docker pull mongo:7.0
```

## Environment Variables

The Docker setup handles environment variables through the docker-compose.yml file. The application expects:
- `MONGODB_URL`: Set to `mongodb://mongodb:27007` for internal container communication
- `MONGODB_DATABASE`: Set to `mini_rag` for the database name

## Data Persistence

MongoDB data is persisted in the `./mongodb_data` directory relative to the docker-compose.yml file location. This ensures data persists between container restarts.