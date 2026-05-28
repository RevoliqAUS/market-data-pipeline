#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI-powered market analytics pipeline.")
    parser.add_argument("--no-ai", action="store_true", help="Skip OpenAI summary generation.")
    args = parser.parse_args()

    from orchestration.pipeline import run_pipeline

    result = run_pipeline(use_ai=not args.no_ai)
    print(json.dumps({"date": result["date"], "paths": result["paths"]}, indent=2))


if __name__ == "__main__":
    main()
