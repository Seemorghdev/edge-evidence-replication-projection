# Validation receipt

This history-free public projection is validated as a self-contained, credential-free reviewer surface.

## Required checks

```bash
python -m pip install -e '.[dev]'
make test
python -m compileall -q apps packages replication demo
python scripts/check_standalone.py
python -m build
python scripts/check_distribution.py
make demo
make inspect
```

The deterministic demo must prove target creation/re-adoption, exact adoption, immutable creation, independent readback, transient cleanup, deterministic rerun behavior, collision refusal, and preservation of conflicting bytes.

## Authority boundary

Validation must not access credentials, authenticate to a provider, perform Terraform apply, mutate IAM, create cloud resources, deploy workloads, publish releases, or change repository visibility. The Terraform surface is validated with mock/credential-free tooling only.

Generated from a reviewed private canonical source.
