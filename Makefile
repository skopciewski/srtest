
install-hooks:
	@command -v pre-commit >/dev/null 2>&1 || { \
	    echo >&2 "Pre-commit is not installed. Please install it before running this command."; \
	    exit 1; \
	}
	pre-commit install --install-hooks
.PHONY: install-hooks

chaneglog:
ifdef EDITOR
	UNRELEASED_FILE=.unreleased/$(shell date +"%Y%m%d%H%M%S").md; \
	mkdir -p $${UNRELEASED_FILE%/*}; \
	echo -e "---" > $$UNRELEASED_FILE; \
	BRANCH_NAME=$$(git symbolic-ref --short HEAD); \
	BUMP="patch"; \
	if echo $$BRANCH_NAME | grep -Eq '^feature/'; then \
		BUMP="minor"; \
	fi; \
	ISSUE_ID=$$(echo $$BRANCH_NAME | grep -oE '([A-Z]+-[0-9]+)' | head -n 1); \
	if [ -n "$$ISSUE_ID" ]; then \
		echo -e "\nissue: $$ISSUE_ID" >> $$UNRELEASED_FILE; \
	fi; \
	echo -e "bump: $$BUMP" >> $$UNRELEASED_FILE; \
	echo -e "---" >> $$UNRELEASED_FILE; \
	$(EDITOR) $$UNRELEASED_FILE
else
	@echo "EDITOR variable is not defined. Please define it before running this command."
	@exit 1
endif
.PHONY: changelog
