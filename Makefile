.PHONY: install demo test test-all inspect clean docker-build validate

PYTHON ?= python
DEMO_OUTPUT ?= .demo-output

install:
	$(PYTHON) -m pip install -e '.[dev]'

demo:
	$(PYTHON) demo/run_demo.py --output-dir "$(DEMO_OUTPUT)"

test:
	$(PYTHON) -m pytest -q \
	  --ignore=tests/unit/test_replication_gcs.py \
	  -m "not gcs"

test-all:
	$(PYTHON) -m pytest -q

inspect:
	$(PYTHON) scripts/inspect_demo.py --output-dir "$(DEMO_OUTPUT)"

clean:
	$(PYTHON) scripts/clean_demo.py --output-dir "$(DEMO_OUTPUT)"

docker-build:
	docker build -t edge-evidence-replication:local .

validate: test
	$(PYTHON) -m compileall -q apps packages replication demo
