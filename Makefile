.PHONY: install
install:
	uv sync --locked --no-dev

.PHONY: install_dev
install_dev:
	uv sync --locked

.PHONY: upgrade_dependencies
upgrade_dependencies:
	uv sync --upgrade

.PHONY: test
test:
	uv run --locked pytest ./afk_parser/tests -vv

.PHONY: lint
lint:
	uv run --locked pyright .

.PHONY: format
format:
	uv run --locked ruff format .

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
