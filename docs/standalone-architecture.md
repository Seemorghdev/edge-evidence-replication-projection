# Standalone architecture

This repository packages the bounded replication worker as an independent component with preserved core behavior.

## Authority flow

```text
finalized SQLite row + immutable source bytes
                 |
                 v
      source eligibility / target binding
                 |
          +------+------+
          |             |
    exact target     absent target
      bytes             bytes
          |             |
       adopt       exclusive create
          +------+------+
                 |
                 v
        independent target readback
                 |
                 v
        canonical SQLite result
```

The worker owns deterministic convergence of finalized immutable evidence objects to an already-bound target. It does not capture or process evidence, select or provision a target, create credentials, change IAM, create buckets, schedule itself, expose an operator API, or become evidence authority.

SQLite and immutable filesystem/object bytes are authoritative. CLI summaries and demo receipts are deterministic projections of that state; they do not replace the underlying authority.

## Binding and publication semantics

Before replication, the worker requires the configured target ID to match the canonical target row and requires the adapter/runtime target identity to match the previously bound marker. A mismatch fails closed.

For each eligible object, the provider-neutral core accepts only two successful destination states:

- the exact expected bytes already exist and are independently verified, so the object is adopted; or
- the destination is absent and the adapter performs an exclusive immutable create followed by independent verification.

Existing non-matching bytes are a collision. The worker reports `destination_collision` and does not overwrite, delete, or repair the conflicting object. Retry and reconciliation operate from canonical replica state rather than creating a second checkpoint authority.

## Provider boundary

The core depends on the `ReplicationTarget` contract, not provider SDK types. Mounted NFSv4 is the filesystem adapter. GCS is optional, lazily imported, and requires the separate `gcs` dependency extra; provider credentials remain ambient runtime inputs outside the core.

Terraform under `terraform/` is an illustrative Cloud Run Job shape only. It has no IAM, credential, bucket, API-enablement, state-backend, or apply authority.

## Local proof boundary

The deterministic demo uses synthetic finalized evidence, local SQLite authority, and an ordinary local target directory. It temporarily substitutes only the NFSv4 mount-type probe so reviewers do not need a real NFS service; publication, collision refusal, transient cleanup, SQLite state transitions, and byte readback use the actual replication code paths.

The demo proves exact adoption, immutable creation, independent readback, idempotent rerun behavior, and collision refusal. `.demo-output/summary.json` is machine-readable derived evidence; inspectable SQLite databases and target files remain underneath it.

## AI / agent boundary

Agent policy/contracts may inspect or explain replication proposals, but AI/ADK is not the execution mechanism and is not evidence authority. A model cannot silently provision a provider, change target binding, approve a collision, weaken immutability, or substitute its judgment for deterministic readback.

## Public projection boundary

The public surface preserves the worker, adapters, contracts, deterministic proof, and fail-closed semantics. Authority-bearing private implementation identity values are omitted; the exact-action identity path therefore remains fail-closed in this projection rather than gaining replacement authority.
