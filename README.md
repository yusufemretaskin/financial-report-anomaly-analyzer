# Financial Report Anomaly Analyzer

This is a small FastAPI project that analyzes financial report CSV files.

I built this project to practice Python, FastAPI, pandas, anomaly detection and LLM integration.

## What It Does

- Upload financial report CSV
- Read report data with pandas
- Validate required columns
- Calculate daily changes
- Detect unusual movements
- Return anomaly list
- Generate LLM summary for detected anomalies

## Tech Stack

- Python
- FastAPI
- Uvicorn
- pandas
- OpenAI compatible API / GitHub Models

## Report Flow

```text
Upload CSV report
↓
Read file with pandas
↓
Validate columns
↓
Sort by account / clearer / product / date
↓
Calculate daily changes
↓
Detect anomalies by threshold
↓
Return anomaly list
↓
LLM explains anomalies
```

## Project Structure

```text
app/
  main.py
  api/v1/
    health.py
    reports.py
  services/
    report_analyzer.py
    llm_service.py

sample_reports/
requirements.txt
README.md
```

## Sample Report Columns

```text
date
account
clearer
product
currency
cash_balance
variation_margin
initial_margin
pnl
```

## Health

```http
GET /api/v1/health
```

## Upload Report

```http
POST /api/v1/reports/upload
```

Body type:

```text
form-data
key: file
```

Example:

```bash
curl -X POST \
  -F "file=@sample_reports/daily_financial_report.csv" \
  https://your-codespace-url-8000.app.github.dev/api/v1/reports/upload
```

## Get Uploaded Reports

```http
GET /api/v1/reports
```

## Get Report Anomalies

```http
GET /api/v1/reports/{file_name}/anomalies
```

Example:

```bash
curl https://your-codespace-url-8000.app.github.dev/api/v1/reports/daily_financial_report.csv/anomalies
```

## Get AI Summary

```http
GET /api/v1/reports/{file_name}/summary
```

Example:

```bash
curl https://your-codespace-url-8000.app.github.dev/api/v1/reports/daily_financial_report.csv/summary
```

## Install Packages

```bash
pip install -r requirements.txt
```

## Set Token

```bash
export GITHUB_TOKEN="your-llm-token"
```

## Run API

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Swagger

After running the API, open:

```text
/docs
```

## Current Anomaly Rules

The project detects anomalies using threshold-based rules.

Example thresholds:

```text
cash_balance change >= 50000
variation_margin change >= 10000
initial_margin change >= 5000
pnl change >= 5000
```

## Example Output

```json
{
  "file_name": "daily_financial_report.csv",
  "result": {
    "row_count": 12,
    "anomaly_count": 2,
    "anomalies": [
      {
        "date": "2026-05-03",
        "account": "ACC001",
        "clearer": "CME",
        "product": "WTI",
        "currency": "USD",
        "cash_balance": 30000,
        "variation_margin": -18000,
        "initial_margin": 26000,
        "pnl": -9500,
        "reasons": [
          {
            "field": "cash_balance",
            "change": -55000,
            "threshold": 50000
          }
        ]
      }
    ]
  }
}
```


## Project Summary

This project uses pandas to detect financial report anomalies and uses an LLM to explain the detected issues in business-friendly language.

The anomaly detection is rule-based and deterministic. The LLM is only used for explanation, not for detecting the anomalies.