.PHONY: generate validate test release clean

generate:
	python scripts/build_generated.py

validate:
	python scripts/validate_all.py

test:
	pytest -q

release:
	python scripts/build_release.py

clean:
	rm -rf site .pytest_cache scripts/__pycache__ tests/__pycache__
	find dist -type f ! -name .gitkeep -delete
