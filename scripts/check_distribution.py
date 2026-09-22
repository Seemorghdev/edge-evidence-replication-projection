"""Validate public package metadata and bundled license files."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile


def main() -> int:
    wheels = sorted(Path("dist").glob("*.whl"))
    assert len(wheels) == 1, "expected exactly one wheel"
    with ZipFile(wheels[0]) as archive:
        names = archive.namelist()
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        assert len(metadata_names) == 1
        metadata = archive.read(metadata_names[0]).decode("utf-8")
        assert "License-Expression: MIT" in metadata
        assert "License-File: LICENSE" in metadata
        assert "License-File: THIRD_PARTY_NOTICES.md" in metadata
        assert any(name.endswith(".dist-info/licenses/LICENSE") for name in names)
        assert any(
            name.endswith(".dist-info/licenses/THIRD_PARTY_NOTICES.md")
            for name in names
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
