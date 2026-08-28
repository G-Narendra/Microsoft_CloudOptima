# CloudOptima — production container

# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /build
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml README.md ./
COPY cloudoptima ./cloudoptima

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install .

# Stage 2: slim runtime
FROM python:3.11-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    DEMO_MODE=true \
    LLM_PROVIDER=mock

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 cloudoptima \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin cloudoptima

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/cloudoptima ./cloudoptima

USER cloudoptima

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "cloudoptima/dashboard.py", \
     "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
