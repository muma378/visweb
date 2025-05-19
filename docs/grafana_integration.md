# Grafana Integration Guide

This guide will help you set up Grafana to visualize the data collected by the VisWeb API.

## Prerequisites

- VisWeb API running
- Grafana installed (either locally or a hosted instance)
- Access to the SQLite database file

## Setup Steps

### 1. Install Grafana

If you don't have Grafana installed yet, you can follow the official installation guide:
https://grafana.com/docs/grafana/latest/installation/

For a quick local test, you can use Docker:

```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana-oss
```

### 2. Install SQLite Plugin for Grafana

Grafana doesn't support SQLite out of the box, so you'll need to install a plugin. The recommended plugin is "frser-sqlite-datasource".

From your Grafana instance:

1. Go to Configuration > Plugins
2. Search for "sqlite"
3. Install the "frser-sqlite-datasource" plugin
4. Restart Grafana if required

Alternatively, you can install it via CLI:

```bash
grafana-cli plugins install frser-sqlite-datasource
```

### 3. Configure Data Source

1. In Grafana, go to Configuration > Data Sources
2. Click "Add data source"
3. Select "SQLite" from the list
4. Configure the data source:
   - Name: VisWeb SQLite
   - Path: Enter the absolute path to your SQLite database file (e.g., `/path/to/visweb/data/visweb.db`)
5. Click "Save & Test" to verify the connection

### 4. Create Dashboards

Now you can create dashboards to visualize your health metrics and exercise data. Here are some example queries to get you started:

#### Weight Tracking Dashboard

```sql
SELECT strftime('%Y-%m-%dT%H:%M:%SZ', SUBSTR(recorded_at, 1, 19)) as time, value
FROM health_metrics
JOIN metric_types ON health_metrics.metric_type_id = metric_types.id
WHERE user_id = 1 AND metric_types.name = 'weight'
ORDER BY recorded_at
```

#### Activity Summary Dashboard

```sql
SELECT 
  exercise_records.recorded_at AS time, 
  exercise_types.name AS exercise,
  exercise_records.duration,
  exercise_records.distance,
  exercise_records.calories
FROM exercise_records
JOIN exercise_types ON exercise_records.exercise_type_id = exercise_types.id
WHERE user_id = 1
ORDER BY recorded_at DESC
LIMIT 20
```

#### Daily Steps Dashboard

```sql
SELECT recorded_at AS time, value AS steps
FROM health_metrics
JOIN metric_types ON health_metrics.metric_type_id = metric_types.id
WHERE user_id = 1 AND metric_types.name = 'steps'
ORDER BY recorded_at
```

### 5. Set Up Alerts (Optional)

You can set up alerts in Grafana to notify you when certain conditions are met. For example:

- Alert when no exercise has been recorded for 3 days
- Alert when weight increases by more than 2kg in a week
- Alert when sleep is consistently below 6 hours

## Sample Dashboard JSON

You can import a sample dashboard by going to Dashboard > Import and pasting the JSON from `dashboards/sample_dashboard.json`.

## Troubleshooting

- **Cannot connect to SQLite database**: Make sure the database file path is correct and Grafana has read access to it.
- **No data showing in graphs**: Verify that your queries are correct and that there is data in the database for the specified user.
- **Timestamps showing incorrectly**: Ensure your timestamps are in UTC or adjust the timezone settings in Grafana.
