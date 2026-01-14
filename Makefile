prepare-env:
	./.devcontainer/scripts/prepare-env.sh

run:
	@echo "Starting MCP Server..."
	python -m compileall . -q && python -m sse_mcp_server.main & tail -f /dev/null

redis:
	docker run -d --name redis -p 6379:6379 redis:alpine

test:
	python -m pytest tests/ -v --tb=short

test-coverage:
	coverage run -m pytest && coverage report -m

lint:
	pylint app frontend --fail-under=9.0 --fail-on=E

gen-docs:
	python export-openapi.py app.main:app

install:
	uv pip install --system --upgrade -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -deletema