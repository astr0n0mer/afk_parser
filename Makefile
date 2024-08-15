.venv:
	python -m venv .venv

.PHONY: source_env
source_env: .venv
	. .venv/bin/activate

requirements.txt: source_env
	pip-compile --output-file requirements.txt requirements.in

.PHONY: install
install:
	source .venv/bin/activate && \
	pip install -r requirements.txt
