.venv:
	python -m venv .venv

requirements.txt: .venv requirements.in
	. .venv/bin/activate && \
	pip-compile --output-file requirements.txt requirements.in

requirements-dev.txt: .venv requirements.in requirements-dev.in
	. .venv/bin/activate && \
	pip-compile --output-file requirements-dev.txt requirements.in requirements-dev.in

.PHONY: requirements
requirements: requirements.txt requirements-dev.txt

.PHONY: install
install: .venv
	. .venv/bin/activate && \
	pip install -r requirements.txt

.PHONY: install_dev
install_dev: install
	. .venv/bin/activate && \
	pip install -r requirements-dev.txt

.PHONY: test
test: install_dev
	. .venv/bin/activate && \
	pytest ./afk_parser/tests -vv

.PHONY: lint
lint:
	. .venv/bin/activate && \
	pyright .

.PHONY: format
format:
	. .venv/bin/activate && \
	ruff format .

.PHONY: update_tag_latest
update_tag_latest:
	git tag --delete latest && git push --delete origin latest
	git tag latest && git push origin latest

.PHONY: update_tag_stable
update_tag_stable:
	git tag --delete stable && git push --delete origin stable
	git tag stable && git push origin stable
