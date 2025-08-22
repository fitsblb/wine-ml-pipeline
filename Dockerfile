# ---------- builder ----------
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

# 1) deps first
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# 2) package + source (non-editable install)
COPY setup.py ./
COPY src ./src
RUN pip install .

# 3) app code, configs, params, raw data
COPY app.py main.py ./
COPY config ./config
COPY params.yaml ./
COPY artifacts/data_ingestion ./artifacts/data_ingestion

# 3.1) sanity check that our package imports BEFORE running main.py
RUN python - << 'PY'
import sys
import datascience
print("datascience package at:", datascience.__file__)
import datascience.components.data_ingestion as DI
print("import datascience.components OK")
PY

# 4) build artifacts at image build-time
RUN python main.py


# ---------- runtime ----------
FROM python:3.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash appuser

COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:create_app()"]
