"""Package the repository-owned canonical contracts; --check never writes."""
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
for source in sorted((root / "contracts").glob("*.schema.json")):
    target = root / "videoops/schemas" / source.name
    if "--check" in sys.argv:
        if not target.exists() or target.read_bytes() != source.read_bytes():
            raise SystemExit("Packaged schema drift: " + source.name)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
