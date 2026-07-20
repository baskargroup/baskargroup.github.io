# Baskar Group website: developer tasks
# Homebrew Ruby is keg-only, so put it on PATH for every recipe.

RUBY_BIN := /opt/homebrew/opt/ruby/bin
export PATH := $(RUBY_BIN):$(PATH)

.PHONY: serve build json validate sync test help

help:
	@echo "make serve     - build and serve locally at http://localhost:4000 for private review"
	@echo "make build     - build the static site into _site/"
	@echo "make json      - run scripts/bib_to_json.py (Phase 2+)"
	@echo "make validate  - run scripts/validate.py (Phase 2+)"
	@echo "make sync      - run the OpenAlex sync in dry-run (Phase 2+)"
	@echo "make test      - run the Python unit tests (Phase 2+)"

serve:
	bundle exec jekyll serve --host 127.0.0.1 --port 4000 --livereload

build:
	bundle exec jekyll build

json:
	python3 scripts/bib_to_json.py

validate:
	python3 scripts/validate.py

sync:
	python3 scripts/openalex_sync.py --sync --dry-run

test:
	python3 -m pytest tests/ -q
