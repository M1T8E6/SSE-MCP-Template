prepare-env:
	./.devcontainer/scripts/prepare-env.sh

run:
	@echo "Starting MCP Server..."
	PYTHONPATH=/app/src python -m compileall . -q && PYTHONPATH=/app/src python -m sse_mcp_server.main & tail -f /dev/null

test:
	PYTHONPATH=/app/src python -m pytest tests/ -v --tb=short

lint:
	python -m pylint src/sse_mcp_server --fail-under=9.0 --fail-on=E

gen-docs:
	python export-openapi.py sse_mcp_server.main:app --app-dir src

install:
	uv pip install --system --upgrade -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -deletema