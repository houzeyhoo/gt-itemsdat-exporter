from abc import ABC, abstractmethod
from typing import TextIO

from itemsdat_exporter.parser import ItemsDat


class Exporter(ABC):
    @abstractmethod
    def export(self, items_dat: ItemsDat, fp: TextIO) -> None:
        pass
