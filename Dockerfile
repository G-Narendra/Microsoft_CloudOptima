# CloudOptima — production container (Phase 12).
#
# Multi-stage build: a builder stage installs every dependency into a clean
# virtualenv (cached separately from the app code), and a slim runtime stage
# copies only that venv + the app source. The final image runs as a non-root
# user with a healthcheck — the shape a real Azure App Service deployment
# expects (external principal-engineer review finding: container packaging was
# the missing operational piece).
#
# Build & run:
#   docker build -t cloudoptima .
#   docker run -p 8501:8501 cloudoptima
#   # then open http://localhost:8501 — demo mode by default, no API keys.

# ── Stage 1: builder ──────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
ENV PIP_NO_CACHE_DIR=1

# Build essentials are only needed to compile wheels in this stage; the slim
# runtime below never gets them.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependencies first (Docker layer caching: only reinstalls when they change).
COPY requirements.txt pyproject.toml README.md ./
COPY cloudoptima ./cloudoptima

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install .

# ── Stage 2: slim runtime ─────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    DEMO_MODE=true \
    LLM_PROVIDER=mock

# curl powers the healthcheck. The app runs as a non-root user so a container
# escape can never get a root shell.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 cloudoptima \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin cloudoptima

WORKDIR /app

# The venv from the builder already contains the installed package; the source
# copy is only needed so `streamlit run cloudoptima/dashboard.py` has a file
# path to execute.
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/cloudoptima ./cloudoptima

USER cloudoptima

EXPOSE 8501

# Streamlit's built-in health endpoint: /_stcore/health
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "cloudoptima/dashboard.py", \
     "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
