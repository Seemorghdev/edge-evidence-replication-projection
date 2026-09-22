from replication import init_target, reconcile, run, verify
from replication.cli import main


def test_standalone_facade_is_thin_and_importable() -> None:
    assert callable(init_target)
    assert callable(reconcile)
    assert callable(run)
    assert callable(verify)
    assert callable(main)
