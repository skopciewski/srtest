
install-hooks:
	@command -v pre-commit >/dev/null 2>&1 || { \
	    echo >&2 "Pre-commit is not installed. Please install it before running this command."; \
	    exit 1; \
	}
	pre-commit install --install-hooks
.PHONY: install-hooks

chaneglog:
ifdef EDITOR
	@UNRELEASED_FILE=.unreleased/$(shell date +"%Y%m%d%H%M%S").md; \
	mkdir -p $${UNRELEASED_FILE%/*}; \
	echo -e "<!---" > $$UNRELEASED_FILE; \
	BRANCH_NAME=$$(git symbolic-ref --short HEAD); \
	BUMP="patch"; \
	if echo $$BRANCH_NAME | grep -Eq '^feature/'; then \
		BUMP="minor"; \
	fi; \
	echo -e "// allowed states: major, minor, patch" >> $$UNRELEASED_FILE; \
	echo -e "- bump: $$BUMP" >> $$UNRELEASED_FILE; \
	ISSUE_ID=""; \
	if echo $$BRANCH_NAME | grep -Eq '^([A-Z]+-[0-9]+)'; then \
		ISSUE_ID=$$(echo $$BRANCH_NAME | grep -oE '^([A-Z]+-[0-9]+)'); \
	elif echo $$BRANCH_NAME | grep -Eq '/([A-Z]+-[0-9]+)'; then \
		ISSUE_ID=$$(echo $$BRANCH_NAME | grep -oE '/([A-Z]+-[0-9]+)' | cut -c 2-); \
	fi; \
	if [ -n "$$ISSUE_ID" ]; then \
		echo -e "- ref: $$ISSUE_ID" >> $$UNRELEASED_FILE; \
	fi; \
	echo -e "--->\n" >> $$UNRELEASED_FILE; \
	echo -e "### Notice\n" >> $$UNRELEASED_FILE; \
	echo -e "### Changed\n" >> $$UNRELEASED_FILE; \
	echo -e "### Added\n" >> $$UNRELEASED_FILE; \
	echo -e "### Removed\n" >> $$UNRELEASED_FILE; \
	echo -e "### Fixed\n" >> $$UNRELEASED_FILE; \
	$(EDITOR) $$UNRELEASED_FILE; \
	git add $$UNRELEASED_FILE;
else
	@echo "EDITOR variable is not defined. Please define it before running this command."
	@exit 1
endif
.PHONY: changelog
