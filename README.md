# Microservice CI/CD Demo

A containerized Flask microservice that applies image filters through a simple REST API. The project demonstrates a basic CI/CD workflow using **Python, Flask, Docker, Docker Compose, Pytest, and GitHub Actions**.

## Overview

The service accepts an uploaded image and applies one of several supported filters. It also exposes health and filter-discovery endpoints.

The repository is designed as a practical DevOps/CI-CD demo:

- Flask REST API
- Docker containerization
- Docker Compose for local startup
- Automated tests with Pytest
- GitHub Actions CI/CD pipeline
- Docker Hub image publishing after successful tests on the `main` branch

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Application runtime |
| Flask | REST API |
| Pillow | Image processing |
| Pytest | Automated testing |
| Docker | Containerization |
| Docker Compose | Local container orchestration |
| GitHub Actions | CI/CD automation |
| Docker Hub | Container image registry |

## Project Structure

```text
microservice-cicd-demo/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── app.py
├── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### List Available Filters

```http
GET /filters
```

Example response:

```json
{
  "filters": [
    "blur",
    "sharpen",
    "grayscale",
    "contour",
    "brightness"
  ]
}
```

### Apply an Image Filter

```http
POST /apply?filter=<filter-name>
```

Upload an image using the multipart form field `image`.

Supported filters:

- `blur`
- `sharpen`
- `grayscale`
- `contour`
- `brightness`

Example with cURL:

```bash
curl -X POST \
  -F "image=@sample.jpg" \
  "http://localhost:5000/apply?filter=grayscale" \
  --output filtered.jpg
```

If no filter is specified, the service defaults to `blur`.

## Run Locally with Python

### 1. Clone the repository

```bash
git clone https://github.com/Manik2110/microservice-cicd-demo.git
cd microservice-cicd-demo
```

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
py -3.11 -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

The API will be available at:

```text
http://localhost:5000
```

## Run with Docker

Build the image:

```bash
docker build -t image-filter-service .
```

Run the container:

```bash
docker run -p 5000:5000 image-filter-service
```

The API will be available at:

```text
http://localhost:5000
```

## Run with Docker Compose

Start the service:

```bash
docker compose up --build
```

Run it in the background:

```bash
docker compose up --build -d
```

Stop the service:

```bash
docker compose down
```

## Testing

The project includes automated tests for:

- Health check
- Filter listing
- Successful image processing
- Invalid filter handling
- Requests without an image

Run the tests locally:

```bash
pytest test_app.py -v
```

## CI/CD Pipeline

The GitHub Actions workflow is defined in:

```text
.github/workflows/ci-cd.yml
```

The pipeline runs for pushes and pull requests targeting `main`.

### CI

The test job:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies
4. Runs the Pytest test suite

### CD

For a successful push to `main`, the pipeline:

1. Runs the test job
2. Logs in to Docker Hub using GitHub Actions secrets
3. Builds the Docker image
4. Pushes two tags to Docker Hub:
   - `latest`
   - the Git commit SHA

Required GitHub repository secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The image is published using the repository owner's Docker Hub namespace:

```text
<DOCKERHUB_USERNAME>/image-filter-service:latest
<DOCKERHUB_USERNAME>/image-filter-service:<commit-sha>
```

## CI/CD Flow

```text
Developer
   │
   ▼
Git Push / Pull Request
   │
   ▼
GitHub Actions
   │
   ├── Install dependencies
   │
   ├── Run Pytest
   │
   └── If push to main + tests pass
           │
           ▼
      Build Docker Image
           │
           ▼
        Docker Hub
```

## Error Handling

The API returns a `400 Bad Request` for common client-side errors such as:

- No image uploaded
- Invalid image data
- Unknown filter name

## Future Improvements

Possible extensions for this project include:

- Kubernetes deployment
- Image versioning and release automation
- Container vulnerability scanning
- Deployment to AWS, Azure, or GCP
- Infrastructure as Code with Terraform
- Monitoring and logging
- API documentation with OpenAPI/Swagger
- Separate microservices for upload, processing, and storage

## Learning Goals

This project was built to practice:

- REST API development with Flask
- Containerizing Python applications
- Writing automated tests
- Building CI/CD pipelines with GitHub Actions
- Publishing Docker images
- Understanding the flow from source code to a container registry

## License

This project is available for learning and demonstration purposes.
