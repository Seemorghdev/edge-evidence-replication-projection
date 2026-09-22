# Local operations

## Install and test

```bash
python -m pip install -e '.[dev]'
make test
make demo
make inspect
make clean
```

The base install has no runtime Python dependencies. Runtime, contract, adapter, demo, package, and public-readiness tests remain active.

## Deterministic local proof

`make demo` is the reviewer-facing proof and requires no credentials, network, cloud account, model, or provider service. It writes persistent evidence to `.demo-output/` and prints a human summary.

For machine-readable output:

```bash
python demo/run_demo.py --json
cat .demo-output/summary.json
```

The receipt proves finalized synthetic source input, explicit target binding, exact adoption, immutable create, independent byte-size/SHA-256 readback, transient cleanup, deterministic rerun behavior, and fail-closed collision handling.

The local proof temporarily substitutes the NFSv4 mount-type probe so it can use an ordinary local directory. This is not a live NFS acceptance test.

## CLI

```bash
replication-worker run \
  --database PATH \
  --spool-root PATH \
  --target-config replication.toml

replication-worker verify \
  --database PATH \
  --target-config replication.toml
```

Target configuration is non-secret composition supplied by the operator; provisioning, IAM, credentials, bucket creation, and target selection remain outside the worker.

## Container

```bash
docker build -t edge-evidence-replication:local .
docker run --rm edge-evidence-replication:local --help
```

The image runs as a non-root user and contains the base provider-neutral package, not the optional GCS SDK.

## Terraform

`terraform/` is a sanitized Cloud Run Job example only. It contains no live project/account authority, state backend, credential, IAM, API-enablement, registry, bucket, or deployment authority. `terraform apply` is outside this repository's authorized workflow.

## CI policy

GitHub Actions (`.github/workflows/required.yml`) is the automatic read-only gate for pull requests and `main`. It installs the base dev package, runs tests, compiles Python, executes the public-safety check, builds the distribution, and validates built artifacts.

Travis is manual/API-only. A manual run executes `scripts/ci-heavy.sh` for supported Python versions, optional GCS tests, deterministic demo, package/container/devcontainer validation, credential-free Terraform validation, and Git object integrity.
