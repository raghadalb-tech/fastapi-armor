# fastapi-armor

Production-ready error handling, logging, and monitoring for FastAPI apps.

## Installation

```bash
pip install fastapi-armor
```

## Usage

### Before

```python
from fastapi import FastAPI

app = FastAPI()
```

### After (one line)

```python
from fastapi import FastAPI
from fastapi_armor import Armor

app = FastAPI()
Armor(app)  # Adds error handlers, logging, and optional Sentry
```

### With custom options

```python
Armor(
    app,
    log_file="logs/api.log",
    log_max_bytes=10_000_000,
    log_backup_count=5,
    sentry_dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    environment="production",
)
```

## Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `app` | `FastAPI` | Required | FastAPI application instance to protect. |
| `log_file` | `str` | `"logs/app.log"` | Log file path for rotating logs. |
| `log_max_bytes` | `int` | `5_000_000` | Maximum file size before rotating. |
| `log_backup_count` | `int` | `3` | Number of rotated log files to keep. |
| `sentry_dsn` | `str` | `""` | Sentry DSN. If empty, Sentry is disabled. |
| `environment` | `str` | `"development"` | Sentry environment tag. |

## Requirements

- Python `>=3.9`
- FastAPI `>=0.100.0`
- sentry-sdk with FastAPI integration `>=1.40.0`
