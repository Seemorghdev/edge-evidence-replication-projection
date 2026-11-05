# Edge Evidence Replication

A deterministic, SQLite-authoritative replication worker for finalized immutable evidence.

**Finalized source → replication decision → immutable copy or exact adoption → independent readback → recorded result**

This repository is the recruiter-facing Replication product surface. It starts only from already-finalized source authority and converges eligible objects to one already-bound replica target.

## Repository shape

```text
apps/replication_worker/    CLI and target composition boundary
packages/replication/      provider-neutral core plus NFS and optional GCS adapters
packages/database/         SQLite schema and migrations used by replication
demo/                      credential-free deterministic local proof
tests/                     behavior, contract, demo and readiness tests
docs/                      architecture, operations and validation guidance
terraform/                 sanitized Cloud Run Job configuration example
Dockerfile                 non-root one-shot worker image
.devcontainer/             portable development environment
Makefile                   local validation and demo commands
```

## Product role

Capture, processing, target provisioning, and replication authority remain separate. The worker owns only deterministic convergence of finalized immutable evidence objects to one already-bound target:

1. read finalized object identity from existing SQLite/filesystem authority;
2. require the exact target ID, adapter kind, marker, and runtime binding;
3. decide between exact adoption and immutable publication;
4. refuse conflicting destination bytes rather than overwrite them;
5. independently read back and verify target bytes;
6. record the verified or failed result in canonical SQLite authority.

The worker does not capture or process media, provision storage, create credentials, change IAM, create buckets, choose a target, schedule future work, run as a daemon, expose an operator API, or create a second evidence authority.

AI/ADK is not part of the replication execution or evidence-authority path. Agent contracts can constrain or explain proposed actions, but a model does not silently invoke replication, approve collisions, weaken immutability, or replace SQLite/filesystem evidence.

## Quick start

Python 3.11 or newer is supported. The base install has no runtime Python dependencies and does not install a cloud SDK.

```bash
python -m pip install -e '.[dev]'
make test
make demo
make inspect
```

`make demo` requires no network, credentials, cloud service, model, provider account, or publication access. It creates synthetic finalized input, local SQLite authority, and an ordinary local target directory, then exercises the real replication publication/collision/readback paths. For this credential-free proof only, the demo substitutes the NFSv4 mount-type probe so a real NFS mount is not required; it does not claim to validate a live NFS service.

The machine-readable receipt is `.demo-output/summary.json`.

```bash
python demo/run_demo.py --json
```

The proof covers target creation and safe re-adoption, exact adoption, immutable creation, independent readback, transient-partial cleanup, an idempotent rerun, and refusal to overwrite conflicting bytes.

## Run once

```bash
replication-worker run \
  --database PATH \
  --spool-root PATH \
  --target-config replication.toml

replication-worker verify \
  --database PATH \
  --target-config replication.toml
```

Successful commands emit one machine-readable JSON object. Errors emit a stable finding code and non-zero status. Configuration is supplied by the operator at runtime. Real target IDs, mounts, bucket names, prefixes, account identifiers, tokens, keys, and credential files do not belong in this repository.

## Provider-neutral core and optional GCS

The provider-neutral worker depends on the `ReplicationTarget` contract rather than cloud SDK types. GCS support is optional:

```bash
python -m pip install -e '.[dev,gcs]'
```

The GCS adapter uses provider-standard ambient credentials at runtime and is not credential authority. Unit coverage uses fakes; the portfolio proof requires no provider access.

## Failure semantics

The worker fails closed on target-identity mismatch, destination collision, publication races, corrupt or changed source bytes, corrupt readback, unsafe paths, unavailable/read-only targets, and unsupported exclusive publication. Conflicting destination content is never silently replaced.

## Packaging and infrastructure boundary

- `replication/` is a thin stable facade over the worker modules.
- `Dockerfile` builds a non-root one-shot worker image.
- `.devcontainer/` provides a portable local development environment.
- `terraform/` is a sanitized Cloud Run Job example with no state backend, IAM, credential, API-enablement, registry, bucket, or apply authority.
- `.github/workflows/required.yml` is the pull-request and `main` read-only validation gate.
- `.travis.yml` remains manual/API-only and runs the sequential heavy validation lane.

See `docs/standalone-architecture.md`, `docs/operations.md`, and `docs/validation-receipt.md`.

## Public projection boundary

This public-facing tree contains the product, deterministic proofs, tests, documentation, license/security surfaces, and bounded validation needed by an external reviewer. Authority-bearing private implementation identity values are intentionally unavailable here and fail closed if invoked.

Generated from a reviewed private canonical source.

## Security

Report security-sensitive issues through GitHub Private Vulnerability Reporting rather than a public issue. See `SECURITY.md`.

## License and notices

Licensed under the MIT License. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.
