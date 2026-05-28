#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the optional Prefect orchestration flow locally.")
    parser.add_argument("--no-ai", action="store_true", help="Skip OpenAI summary generation.")
    args = parser.parse_args()

    try:
        from orchestration.prefect_flow import market_data_pipeline_flow
    except ImportError as exc:
        if exc.name == "prefect":
            print(
                "Prefect is not installed. Install project dependencies first:\n"
                "  pip install -r requirements.txt\n\n"
                "Or install only Prefect for the orchestration demo:\n"
                "  pip install prefect",
                file=sys.stderr,
            )
            return 1
        raise

    result = market_data_pipeline_flow(use_ai=not args.no_ai)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

