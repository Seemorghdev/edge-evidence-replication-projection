from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_public_package_metadata_and_notices() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = data["project"]
    assert project["license"] == "MIT"
    assert set(project["license-files"]) == {"LICENSE", "THIRD_PARTY_NOTICES.md"}
    assert data["build-system"]["requires"] == ["setuptools>=82,<83"]
    assert "MIT License" in (ROOT / "LICENSE").read_text()
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text()
    assert "Google Cloud Storage Python client" in notices
    assert "Upstream repository" not in notices
    assert "Upstream commit" not in notices


def test_public_readme_and_security_are_actionable() -> None:
    readme = (ROOT / "README.md").read_text()
    assert (
        "Finalized source → replication decision → immutable copy or exact adoption "
        "→ independent readback → recorded result"
    ) in readme
    assert ".demo-output/summary.json" in readme
    assert "does not claim to validate a live NFS service" in readme
    assert "manual/API-only" in readme
    assert "AI/ADK is not part of the replication execution" in readme
    assert "Generated from a reviewed private canonical source." in readme
    assert "SOURCE_PROVENANCE" not in readme
    assert "EXPORT_PROVENANCE" not in readme
    assert ("generated" + "-product/" + "upstream-first") not in readme
    security = (ROOT / "SECURITY.md").read_text()
    assert "Report a vulnerability" in security
    assert "three business days" in security


def test_architecture_and_operations_match_demo_boundary() -> None:
    architecture = (ROOT / "docs" / "standalone-architecture.md").read_text()
    operations = (ROOT / "docs" / "operations.md").read_text()
    assert "canonical SQLite result" in architecture
    assert "Existing non-matching bytes are a collision" in architecture
    assert "temporarily substitutes only the NFSv4 mount-type probe" in architecture
    assert "not a live NFS acceptance test" in operations
    assert "manual/API-only" in operations


def test_container_and_devcontainer_public_surfaces() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "THIRD_PARTY_NOTICES.md" in dockerfile
    devcontainer = (ROOT / ".devcontainer" / "Dockerfile").read_text()
    assert "ARG TARGETARCH" in devcontainer
    assert "linux_${TARGETARCH}.zip" in devcontainer
    dockerignore = (ROOT / ".dockerignore").read_text()
    assert "**/.terraform" in dockerignore
    assert "**/*.egg-info" in dockerignore


def test_ci_is_read_only_and_heavy_lane_is_manual() -> None:
    workflow = (ROOT / ".github/workflows/required.yml").read_text()
    assert "contents: read" in workflow
    assert "actions/checkout@v7" in workflow
    assert "actions/setup-python@v7" in workflow
    assert "python -m build" in workflow
    travis = (ROOT / ".travis.yml").read_text()
    assert "if: type = api" in travis
    assert "type = push" not in travis
    assert "jobs:" not in travis
    assert "matrix:" not in travis


def test_terraform_example_retains_provider_boundary() -> None:
    main = (ROOT / "terraform" / "main.tf").read_text()
    assert main.count('resource "') == 1
    assert 'resource "google_cloud_run_v2_job"' in main
    readme = (ROOT / "terraform" / "README.md").read_text()
    assert "not authorized for `terraform apply`" in readme


def test_projection_sensitive_artifacts_are_absent() -> None:
    for relative in (
        "SOURCE_PROVENANCE.json",
        "EXPORT_PROVENANCE.json",
        "tests/test_export_metadata.py",
        "tests/test_exported_integration.py",
    ):
        assert not (ROOT / relative).exists()
