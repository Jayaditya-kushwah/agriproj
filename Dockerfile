FROM python:3.11-slim

LABEL maintainer="AgriDoc Contributors"
LABEL description="AgriDoc — Farm Document Digitizer for Telangana Farmers"
LABEL version="1.0.0"

# System dependencies — Tesseract CPU OCR + Indian language packs
# No GPU required. All inference runs on CPU via LSTM engine.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tesseract-ocr \
    tesseract-ocr-tel \
    tesseract-ocr-hin \
    tesseract-ocr-tam \
    tesseract-ocr-kan \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 agridoc
USER agridoc
WORKDIR /home/agridoc/app

# Python dependencies
COPY --chown=agridoc:agridoc pyproject.toml ./
RUN pip install --no-cache-dir --user gunicorn && \
    pip install --no-cache-dir --user -e . 2>/dev/null || true

# Copy application
COPY --chown=agridoc:agridoc . .
RUN pip install --no-cache-dir --user -e .

# Persistent data directories
RUN mkdir -p /home/agridoc/data/uploads

ENV PATH="/home/agridoc/.local/bin:${PATH}"
ENV FLASK_ENV=production
ENV OFFLINE_MODE=true
ENV DATABASE_PATH=/home/agridoc/data/agridoc.db
ENV UPLOAD_FOLDER=/home/agridoc/data/uploads

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Railway injects $PORT at runtime
CMD gunicorn "agridoc.app:create_app()" \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile -
