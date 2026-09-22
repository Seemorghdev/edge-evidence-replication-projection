"""Standalone command entry point delegating to the preserved CLI."""

from apps.replication_worker.cli import main

__all__ = ["main"]

if __name__ == "__main__":
    raise SystemExit(main())
