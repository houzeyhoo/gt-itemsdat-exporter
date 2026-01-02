import sys
from argparse import ArgumentParser, FileType, Namespace
from typing import BinaryIO

from .exporters import CSVExporter, Exporter, JSONExporter
from .parser import parse_items_dat

EXPORTERS: dict[str, Exporter] = {
    "json": JSONExporter(),
    "mjson": JSONExporter(minify=True),
    "psv": CSVExporter(separator="|"),
    "tsv": CSVExporter(separator="\t"),
}


class Arguments(Namespace):
    input: BinaryIO
    format: str = "tsv"
    skip_version_check: bool = False
    discard_bytes: int = 0


def main() -> int:
    parser = ArgumentParser(description="Tool for exporting Growtopia's items.dat file to other formats")

    parser.add_argument(
        "input",
        type=FileType("rb"),
        help="path to the items.dat file",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=EXPORTERS.keys(),
        default="tsv",
        help="export format (default: tsv)",
    )

    parser.add_argument(
        "-V",
        "--skip-version-check",
        action="store_true",
        help="attempt to parse even if the items.dat version is unsupported",
    )

    parser.add_argument(
        "-d",
        "--discard-bytes",
        type=int,
        default=0,
        metavar="N",
        help="discard extra N bytes at the end of every item (default: 0)",
    )
    args = parser.parse_args(namespace=Arguments())

    try:
        with args.input as fp:
            items_dat = parse_items_dat(
                fp,
                skip_version_check=args.skip_version_check,
                discard_bytes=args.discard_bytes,
            )
        exporter = EXPORTERS[args.format]
        exporter.export(items_dat, sys.stdout)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        sys.stderr.close()
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
