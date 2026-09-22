FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN groupadd --system app && useradd --system --gid app --home-dir /app app
WORKDIR /app

COPY pyproject.toml README.md LICENSE THIRD_PARTY_NOTICES.md ./
COPY apps ./apps
COPY packages ./packages
COPY replication ./replication
RUN python -m pip install --no-cache-dir .

USER app
ENTRYPOINT ["replication-worker"]
CMD ["--help"]
