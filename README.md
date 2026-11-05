# Edge Evidence Replication

A deterministic replication worker for finalized immutable evidence, for engineers reviewing bounded copy and verification behavior.

**Status.** Built: a SQLite-authoritative worker that creates an immutable replica or adopts an exact copy, then reads it back independently. Evidence: 59 tests pass; one optional GCS test is deselected by the default test command. The synthetic demo records the sequence “Finalized source → replication decision → immutable copy or exact adoption → independent readback → recorded result”. Limits: the demo needs no cloud service, and does not claim to validate a live NFS service. AI/ADK is not part of the replication execution or evidence-authority path. Generated from a reviewed private canonical source. The sequential `.travis.yml` validation lane remains manual/API-only.

## Quick-start

Python 3.11 or newer with working `venv`/`ensurepip`; no runtime Python dependencies. From the repository root:

```bash
PYTHON="$(python3.12 -c 'import pathlib, sys; print(pathlib.Path(sys.executable).resolve())')"
"$PYTHON" -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python demo
make PYTHON=.venv/bin/python inspect
```

The demo is synthetic and credential-free. Its machine-readable result is `.demo-output/summary.json`.

## Tests

`make test`: 59 passed, 1 deselected. CI: the `required` workflow runs Python 3.12 tests, compile, standalone and package checks. The latest default-branch run passed on 22 September 2026.

## How it fits

Part of [Edge Evidence: copy, adopt, verify](https://mehridian.tech/projects/edge-evidence-replication). It handles only deterministic convergence of already-finalized evidence to a target bound in advance. Technical docs: [Replication readback](https://docs.mehridian.tech/edge-evidence/replication/verification-readback/) and [development and operations](https://docs.mehridian.tech/edge-evidence/development-and-operations/). See the [portfolio overview](docs/portfolio-overview.md) for command use, failure semantics and the component boundary.

## Licence

MIT. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.
