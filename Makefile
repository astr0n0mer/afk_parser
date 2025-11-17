.venv:
	uv venv --clear

.PHONY: install
install: .venv
	. .venv/bin/activate && \
	uv sync --no-dev

.PHONY: install_dev
install_dev: install
	. .venv/bin/activate && \
	uv sync

.PHONY: upgrade_dependencies
upgrade_dependencies: .venv install_dev
	. .venv/bin/activate && \
	uv sync --upgrade

.PHONY: test
test: install_dev
	. .venv/bin/activate && \
	python -m pytest ./afk_parser/tests -vv

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

.PHONY: group_dependabot_prs
group_dependabot_prs:
	git fetch --all & \
	git switch --create grouped_dependency_upgrade && \
	git branch --all | grep dependabot | xargs -I {} git merge {} && \
	gh pr create \
		--title "build(deps): grouped dependabot upgrades" \
		--fill-verbose \
		--assignee "@me"
