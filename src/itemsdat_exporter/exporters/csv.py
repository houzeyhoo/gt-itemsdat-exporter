import csv
from typing import TextIO

from itemsdat_exporter.parser import ItemsDat

from .base import Exporter


class CSVExporter(Exporter):
    def __init__(self, separator) -> None:
        super().__init__()
        self._separator = separator

    def export(self, items_dat: ItemsDat, fp: TextIO) -> None:
        field_names = list(items_dat.items[0].keys()) if items_dat.items else []
        writer = csv.DictWriter(fp, fieldnames=field_names, delimiter=self._separator, lineterminator="\n")
        writer.writeheader()
        writer.writerows(items_dat.items)
