#!/usr/bin/env bash
set -euo pipefail

for version in 3.12 3.13 3.14; do
  venv="/tmp/replication-${version}"
  uv venv --python "${version}" "${venv}"
  uv pip install --python "${venv}/bin/python" -e '.[dev]'
  "${venv}/bin/python" -m pytest -q \
    --ignore=tests/unit/test_replication_gcs.py \
    -m 'not gcs'
  "${venv}/bin/python" -m compileall -q apps packages replication demo
done

uv pip install --python /tmp/replication-3.12/bin/python -e '.[dev,gcs]'
/tmp/replication-3.12/bin/python -m pytest -q \
  tests/unit/test_replication_gcs.py tests/test_integration.py
/tmp/replication-3.12/bin/python scripts/check_standalone.py
rm -rf .demo-output build dist ./*.egg-info
/tmp/replication-3.12/bin/python demo/run_demo.py --output-dir .demo-output
/tmp/replication-3.12/bin/python scripts/inspect_demo.py --output-dir .demo-output
/tmp/replication-3.12/bin/python -m build
/tmp/replication-3.12/bin/python scripts/check_distribution.py
docker build -t edge-evidence-replication:ci .
docker run --rm edge-evidence-replication:ci --help
devcontainer build --workspace-folder .
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false -input=false
terraform -chdir=terraform validate
terraform -chdir=terraform test -verbose
test "$(git rev-list --max-parents=0 HEAD | wc -l | tr -d ' ')" = 1
git fsck --full
