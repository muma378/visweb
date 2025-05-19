# VisWeb

VisWeb is a personal health and fitness tracking API that allows you to log and visualize health metrics and exercise data through a simple API. It was built to make personal data tracking easy with a robust API and Grafana visualization support.

## Features

- RESTful API for tracking health metrics (weight, heart rate, sleep, etc.)
- Track exercise data (running, cycling, etc.) with duration, distance, and calories
- Quick logging via URL parameters for easy data collection
- SQLite database for simple setup and maintenance
- OpenAPI documentation (Swagger UI)
- Grafana integration for data visualization

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Start the application:

```bash
python main.py
```

## Quick Start

After starting the application, you can:

1. Access the API documentation at http://localhost:8000/docs
2. Initialize the database with sample data:

```bash
python scripts/init_db.py
```

3. Log data using the quick log endpoint:

```
http://localhost:8000/api/v1/quick/log?user_id=1&type=weight&value=75.5
```

4. Set up Grafana for visualization (see [Grafana Integration Guide](docs/grafana_integration.md))

## API Endpoints

The API provides the following endpoints:

- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/metric-types/` - List all metric types
- `POST /api/v1/metric-types/` - Create a new metric type
- `GET /api/v1/exercise-types/` - List all exercise types
- `POST /api/v1/exercise-types/` - Create a new exercise type
- `GET /api/v1/health-metrics/` - List health metrics with filters
- `POST /api/v1/health-metrics/` - Create a new health metric
- `GET /api/v1/exercises/` - List exercise records with filters
- `POST /api/v1/exercises/` - Create a new exercise record
- `GET /api/v1/quick/log` - Quick logging via URL parameters

## Data Visualization

This project integrates with Grafana for data visualization. See the [Grafana Integration Guide](docs/grafana_integration.md) for setup instructions and sample dashboards.

## Use Cases

- Personal health tracking (weight, sleep, heart rate)
- Fitness tracking (running, cycling, workouts)
- Long-term health trends analysis
- Setting and monitoring health goals

## License

MIT