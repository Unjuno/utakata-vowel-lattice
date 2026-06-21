.PHONY: setup install-dev test demo analyze-demo doctor clean

PYTHON ?= python
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	$(PY) scripts/doctor.py

install-dev:
	$(PIP) install -e ".[dev]"

test:
	$(PY) -m pytest

demo:
	$(PY) scripts/generate_events.py --seed 20260621 --steps 16 --output outputs/render_events.json

analyze-demo: demo
	$(PY) scripts/analyze_sequence.py --input outputs/render_events.json --json-report outputs/analysis/sequence.json --md-report outputs/analysis/sequence.md

doctor:
	$(PY) scripts/doctor.py

clean:
	rm -rf outputs .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
