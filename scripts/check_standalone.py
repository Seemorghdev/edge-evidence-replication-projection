"""Public-projection privacy, credential, and CI-boundary checks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".demo-output", "__pycache__", ".pytest_cache", "build", "dist"}
FORBIDDEN_PATHS = {
    "SOURCE_PROVENANCE.json",
    "EXPORT_PROVENANCE.json",
    "tests/test_export_metadata.py",
    "tests/test_exported_integration.py",
}
FORBIDDEN_PHRASES = (
    "generated" + "-product/" + "upstream-first",
    "public " + "snapshot",
    "export" + "-only",
    "generated" + "-public",
    "private-" + "redacted",
)
SAFE_PROVENANCE = "Generated from a reviewed private canonical source."

SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.I),
    re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b"),
    re.compile(r"\bgithub_pat_[0-9A-Za-z_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
)
SERVICE_ACCOUNT = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.iam\.gserviceaccount\.com\b", re.I)
REGISTRY_COORD = re.compile(r"\b[a-z0-9-]+-docker\.pkg\.dev/[A-Za-z0-9._/-]+", re.I)
SHA1_LITERAL = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.I)


def main() -> int:
    for relative in FORBIDDEN_PATHS:
        assert not (ROOT / relative).exists(), f"publication-sensitive path present: {relative}"

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        relative = path.relative_to(ROOT).as_posix()
        owner_slash = "Seemorgh" + "dev/"
        assert owner_slash not in text, f"repository coordinate found in {relative}"
        assert not SHA1_LITERAL.search(text), f"exact git object identifier found in {relative}"
        for phrase in FORBIDDEN_PHRASES:
            assert phrase.lower() not in text.lower(), f"stale lineage wording in {relative}: {phrase}"
        for pattern in SECRET_PATTERNS:
            assert not pattern.search(text), f"secret-shaped content in {relative}"

        for line in text.splitlines():
            if SERVICE_ACCOUNT.search(line):
                assert "example-project" in line, f"non-placeholder service-account coordinate in {relative}"
            if REGISTRY_COORD.search(line):
                assert "example-project" in line, f"non-placeholder registry coordinate in {relative}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert SAFE_PROVENANCE in readme
    assert readme.count(SAFE_PROVENANCE) == 1

    workflow = (ROOT / ".github/workflows/required.yml").read_text(encoding="utf-8")
    assert "contents: read" in workflow
    for forbidden in (
        "contents: write",
        "id-token: write",
        "issues: write",
        "pull-requests: write",
        "packages: write",
        "deployments: write",
    ):
        assert forbidden not in workflow

    identity = (ROOT / "packages/replication/action/implementation_identity.py").read_text(encoding="utf-8")
    assert 'CANONICAL_REPOSITORY_ID = "projection-disabled"' in identity
    assert 'CANONICAL_REPOSITORY_FULL_NAME = "projection-disabled"' in identity
    assert 'ACCEPTED_PLAN_COMMIT = "projection-disabled"' in identity
    assert 'ACCEPTED_PLAN_TREE = "projection-disabled"' in identity
    assert 'ACCEPTED_PLAN_DOCUMENT_PATH = "projection-disabled"' in identity
    assert 'ACCEPTED_PLAN_DOCUMENT_BLOB_SHA = "projection-disabled"' in identity

    print("Public projection validation PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
