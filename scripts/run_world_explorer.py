from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from awg_world_explorer import load_review_bundle, serve  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only World Explorer projection service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--print-context", action="store_true", help="Print bundle context and exit")
    args = parser.parse_args()

    bundle = load_review_bundle()
    if args.print_context:
        print(json.dumps(bundle.context(), indent=2, sort_keys=True))
        return

    print(
        json.dumps(
            {
                "service": "world-explorer",
                "host": args.host,
                "port": args.port,
                "read_only": True,
                "bundle_id": bundle.bundle_id,
            },
            indent=2,
            sort_keys=True,
        )
    )
    serve(host=args.host, port=args.port, bundle=bundle)


if __name__ == "__main__":
    main()
