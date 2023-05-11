# ebay-scraper

## Development

1. Frontend

- cd frontend
- npm install
- npm start

2. Backend

- cd backend
- python -m venv venv
- source venv/bin/activate
- uvicorn main:app --reload

## Docker

- `docker-compose.yml` file that defines two services: frontend and backend.
- The frontend service is for React application and the backend service is for FastAPI application.
  When you run the `docker-compose up` command, Docker Compose will read the docker-compose.yml file and start both services in separate containers.
- The two services can interact with each other using their service names as hostnames.
  - For example, from the frontend service, you can send requests to the backend service using the URL http://backend:8000. This is because Docker Compose creates a default network for your application and automatically assigns each service a hostname that matches its service name.
- If any changes are made, `docker-compose down` and then `docker-compose up` again inside directory where yml file is present.

## Modular Backend Structure (future)

```
backend/
    __init__.py
    main.py
    email/
        __init__.py
        sender.py
    scraping/
        __init__.py
        scraper.py
    schedule/
        __init__.py
        runner.py
```
