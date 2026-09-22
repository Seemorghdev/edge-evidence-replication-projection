FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl git make unzip \
    && rm -rf /var/lib/apt/lists/*

ARG TERRAFORM_VERSION=1.16.0
ARG TARGETARCH
RUN curl -fsSLo /tmp/terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TARGETARCH}.zip" \
    && unzip -q /tmp/terraform.zip -d /usr/local/bin \
    && rm /tmp/terraform.zip

WORKDIR /workspace/replication-worker
COPY . .
RUN python -m pip install --no-cache-dir -e '.[dev]'

CMD ["bash"]
