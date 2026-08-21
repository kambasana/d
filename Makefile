.PHONY: generate validate test mvp1 release clean

PYTHON ?= python3

generate:
	PYTHONPATH=scripts $(PYTHON) scripts/build_generated.py

validate:
	PYTHONPATH=scripts $(PYTHON) scripts/validate_all.py

test:
	PYTHONPATH=scripts $(PYTHON) -m pytest -q

mvp1:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp1.py

release:
	PYTHONPATH=scripts $(PYTHON) scripts/build_release.py

clean:
	rm -rf site .pytest_cache scripts/__pycache__ tests/__pycache__
	find dist -type f ! -name .gitkeep -delete
