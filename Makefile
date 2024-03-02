
install-hooks:
	@command -v pre-commit >/dev/null 2>&1 || { \
	    echo >&2 "Pre-commit is not installed. Please install it before running this command."; \
	    exit 1; \
	}
	pre-commit install --install-hooks
.PHONY: install-hooks
