curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh
uv venv
source .venv/bin/activate
uv sync --dev
