from __future__ import annotations

import argparse
import json
import sys

from .ast_parser import parse_file, parse_source


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse Python source using Python's ast module")
    parser.add_argument("path", nargs="?", help="Path to a Python source file")
    parser.add_argument("--stdin", action="store_true", help="Read Python source from stdin")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation level")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.stdin:
        source = sys.stdin.read()
        result = parse_source(source, filename="<stdin>")
    elif args.path:
        result = parse_file(args.path)
    else:
        parser.error("provide a path or use --stdin")

    json.dump(result, sys.stdout, indent=args.indent)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
