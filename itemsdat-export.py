import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from itemsdat_exporter.main import main  # type: ignore

if __name__ == "__main__":
    sys.exit(main())
