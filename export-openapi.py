import argparse
import json
import os
import sys

import yaml
from uvicorn.importer import import_from_string

parser = argparse.ArgumentParser(prog="extract-openapi.py")
parser.add_argument("src", help='App import string. Eg. "main:app"', default="main:app")
parser.add_argument("--app-dir", help="Directory containing the app", default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.app_dir is not None:
        print(f"adding {args.app_dir} to sys.path")
        sys.path.insert(0, args.app_dir)

    print(f"importing app from {args.src}")
    app = import_from_string(args.src)
    # If it's a callable (factory function), call it
    if callable(app) and not hasattr(app, "openapi"):
        app = app()
    openapi = app.openapi()

    app_port = os.environ.get("APP_PORT", "8000")
    SERVER_URL = f"http://localhost:{app_port}"
    openapi["servers"] = [{"url": SERVER_URL}]

    version = openapi.get("openapi", "unknown version")

    os.makedirs("docs", exist_ok=True)
    print(f"writing openapi spec v{version}")

    with open("docs/openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi, f, indent=2)

    with open("docs/openapi.yaml", "w", encoding="utf-8") as f:
        yaml.dump(openapi, f, sort_keys=False)

    print("spec written to docs folder")
