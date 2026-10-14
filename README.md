# CloudPulse ☁️

### Cloud-Based Data Analysis and ML Anomaly Detection Platform

CloudPulse is a containerized FastAPI application that analyzes uploaded CSV data and identifies unusual numeric values using machine learning. It is designed to demonstrate modern application deployment practices using Docker, Kubernetes, and automated CI/CD.

## 🚀 Features

- **REST API:** Built with FastAPI.
- **Health Monitoring:** Health-check endpoint for application availability.
- **CSV Upload:** Upload CSV files for data analysis.
- **Machine Learning:** Uses the Isolation Forest algorithm to detect anomalies in numeric data.
- **Containerization:** Packages the application using Docker.
- **Kubernetes Deployment:** Runs multiple application replicas with readiness and liveness probes.
- **CI/CD:** GitHub Actions automates testing and container image publishing to GitHub Container Registry.
- **Configuration Management:** Uses Kubernetes ConfigMaps and Secrets.
- **Resource Management:** Defines CPU and memory requests and limits.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API framework |
| Pandas | CSV and data processing |
| Scikit-learn | Machine learning and anomaly detection |
| Docker | Application containerization |
| Kubernetes | Container orchestration |
| GitHub Actions | CI/CD automation |
| GitHub Container Registry | Container image storage |
| Terraform | Infrastructure as code exploration |
| Pytest | Automated testing |

## 🏗️ Architecture

1. A user sends a CSV file to the CloudPulse API.
2. FastAPI receives the request and processes the data.
3. Pandas handles the tabular data.
4. Isolation Forest identifies potentially unusual numeric values.
5. The API returns a JSON response containing the analysis results.
6. Docker packages the application, and Kubernetes manages its replicas.
7. GitHub Actions runs tests and builds and publishes container images.

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/upload` | Upload a file |
| POST | `/analyze` | Analyze uploaded data |
| POST | `/detect-anomalies` | Detect anomalies in CSV data |

### Example: Health Check

```json
{
  "status": "healthy",
  "application": "CloudPulse",
  "environment": "production"
}
```

### Example: Anomaly Detection

Send a CSV file containing a numeric `score` column to `/detect-anomalies`.

```bash
curl -X POST http://localhost:8000/detect-anomalies \
  -F "file=@app/test.csv"
```

The response includes the model name, number of rows analyzed, number of detected anomalies, and flagged values.

## 🐳 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Aryank-droid/cloudpulse.git
cd cloudpulse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
uvicorn main:app --app-dir app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/health` in your browser.

Interactive API documentation is available at `http://localhost:8000/docs`.

## 🐳 Run with Docker

Build the image from the project root:

```bash
docker build -t cloudpulse:local .
```

Start the container:

```bash
docker run --rm -p 8000:8000 cloudpulse:local
```

Visit `http://localhost:8000/health`.

## ☸️ Kubernetes

CloudPulse includes Kubernetes manifests in the `k8s/` directory for deployment, service exposure, configuration, and pod management.

Check deployment status:

```bash
kubectl get deployment cloudpulse
kubectl get pods -o wide
kubectl get service cloudpulse-service
```

The deployment is configured with three replicas and application health probes.

## 🔄 CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/ci-cd.yml` automates the project pipeline:

1. Install dependencies.
2. Run automated tests.
3. Build the Docker image.
4. Publish the container image to GitHub Container Registry.

## 🧪 Testing

Run the automated test suite:

```bash
pip install -r requirements-dev.txt
pytest -v
```

## 📁 Project Structure

```text
cloudpulse/
├── app/
│   ├── main.py
│   └── test.csv
├── k8s/
├── terraform/
├── tests/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

## 🎯 Project Goals

CloudPulse demonstrates practical skills in backend API development, machine learning integration, Docker containerization, Kubernetes orchestration, automated testing, CI/CD, and infrastructure as code.

## 👨‍💻 Author

**Aryan Kharat**

GitHub: [Aryank-droid](https://github.com/Aryank-droid)

Project: [CloudPulse](https://github.com/Aryank-droid/cloudpulse)