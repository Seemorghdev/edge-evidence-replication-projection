# Dependency boundary

Component: `replication-worker`
Entry point: `apps.replication_worker.cli:main`

## Included product roots

- `apps/replication_worker/`
- `packages/agent_contracts/`
- `packages/database/`
- `packages/replication/`
- `replication/`
- `demo/`
- `tests/`
- `terraform/`

## External prerequisites

The base runtime has no Python runtime dependency. Optional GCS support is installed through the `gcs` extra and uses ambient provider credentials supplied outside this repository.

The public product does not include deploy roots, live infrastructure authority, credential files, IAM mutation, or provider account coordinates.
