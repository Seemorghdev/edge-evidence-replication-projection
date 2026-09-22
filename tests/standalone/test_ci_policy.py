from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_travis_is_manual_api_only() -> None:
    text = (ROOT / ".travis.yml").read_text(encoding="utf-8")
    assert "if: type = api" in text
    assert "type = push" not in text
    assert "jobs:" not in text
    assert "matrix:" not in text
    assert "type = pull_request" not in text
