.PHONY: generate validate test workflow-check workflow-status workflow-next workflow-graph workflow-run workflow-loop mvp1 mvp2 mvp3 mvp4 mvp5 release clean

PYTHON ?= python3

generate:
	PYTHONPATH=scripts $(PYTHON) scripts/build_generated.py

validate:
	PYTHONPATH=scripts $(PYTHON) scripts/validate_all.py

test:
	PYTHONPATH=scripts $(PYTHON) -m pytest -q

workflow-check:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py validate

workflow-status:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py status

workflow-next:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py next

workflow-graph:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py graph

workflow-run:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py run

workflow-loop:
	PYTHONPATH=scripts $(PYTHON) scripts/stage_workflow.py loop

mvp1:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp1.py

mvp2:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp2.py

mvp3:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp3.py

mvp4:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp4.py

mvp5:
	PYTHONPATH=scripts $(PYTHON) scripts/run_mvp5.py

release:
	PYTHONPATH=scripts $(PYTHON) scripts/build_release.py

clean:
	rm -rf site .pytest_cache scripts/__pycache__ tests/__pycache__
	find dist -type f ! -name .gitkeep -delete
