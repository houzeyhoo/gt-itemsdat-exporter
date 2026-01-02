import json
from typing import TextIO

from itemsdat_exporter.parser import ItemsDat

from .base import Exporter


class JSONExporter(Exporter):
    def __init__(self, minify: bool = False) -> None:
        super().__init__()
        self._minify = minify

    def export(self, items_dat: ItemsDat, fp: TextIO) -> None:
        output = {
            "version": items_dat.version,
            "item_count": items_dat.item_count,
            "items": items_dat.items,
        }
        if self._minify:
            json.dump(output, fp, separators=(",", ":"))
        else:
            json.dump(output, fp, indent=4)
