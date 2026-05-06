# fastapi-armor 🛡️

> Production-ready error handling, logging, and Sentry monitoring for FastAPI — in one line.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/fastapi-armor.svg)](https://pypi.org/project/fastapi-armor/)

---

## Why fastapi-armor?

Every production FastAPI app needs the same boilerplate: structured logging, clean error responses, and error monitoring. **fastapi-armor** wires all of that up automatically — no copy-pasting, no missing edge cases.

**Before:**
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging, logging.handlers, sentry_sdk
# ... 60+ lines of setup code

app = FastAPI()
```

**After:**
```python
from fastapi import FastAPI
from fastapi_armor import Armor

app = FastAPI()
Armor(app)  # ✅ Done.
```

---

## Installation

```bash
pip install fastapi-armor-lib
```

---

## Quick Start

```python
from fastapi import FastAPI
from fastapi_armor import Armor

app = FastAPI()

Armor(
    app,
    log_file="logs/app.log",
    sentry_dsn="https://your-dsn@sentry.io/123",  # optional
    environment="production",
)

@app.get("/")
def root():
    return {"status": "running"}
```

That's it. Your app now has:
- ✅ Rotating file logs + console output
- ✅ Clean JSON error responses for all exception types
- ✅ Sentry integration (if DSN is provided)

---

## What It Does

### 🔴 Error Handling

| Exception Type | Response |
|---|---|
| `HTTPException` | `{"detail": "..."}` with original status code |
| `RequestValidationError` | `{"error": "Validation failed", "detail": [...]}` with 422 |
| Any other `Exception` | `{"error": "Internal server error"}` with 500 (full traceback logged internally) |

All responses use `Content-Type: application/json; charset=utf-8`.

### 📋 Logging

- **Rotating file logs** — auto-creates the `logs/` directory
- **Console output** — for local development
- **Format:** `2024-01-01 12:00:00 | ERROR | Traceback (most recent call last): ...`
- Named logger: `fastapi_armor`

### 🔍 Sentry (optional)

Initializes `sentry_sdk` with `FastApiIntegration` and `StarletteIntegration` when a DSN is provided. Private data is not sent by default.

---

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app` | `FastAPI` | required | Your FastAPI application instance |
| `log_file` | `str` | `"logs/app.log"` | Path to the rotating log file |
| `log_max_bytes` | `int` | `5_000_000` | Max size per log file (5 MB) |
| `log_backup_count` | `int` | `3` | Number of backup log files to keep |
| `sentry_dsn` | `str` | `""` | Sentry DSN — leave empty to disable |
| `environment` | `str` | `"development"` | Environment tag sent to Sentry |

---

## Requirements

- Python 3.9+
- FastAPI 0.100+
- sentry-sdk 1.40+ *(installed automatically)*

---

## Development

```bash
git clone https://github.com/raghadalb-tech/fastapi-armor.git
cd fastapi-armor
pip install -e ".[dev]"
pytest tests/ -v
```

Test output:
