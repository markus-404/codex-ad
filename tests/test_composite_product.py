import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/ad-maker/skills/ad-maker/scripts/composite_product.py"


def test_composite_product_writes_valid_image(tmp_path):
    background = tmp_path / "background.png"
    product = tmp_path / "product.png"
    output = tmp_path / "composited.png"
    Image.new("RGB", (800, 1000), "#337AB7").save(background)
    Image.new("RGBA", (200, 400), (255, 255, 255, 255)).save(product)
    args = [
        sys.executable,
        str(SCRIPT),
        "--background",
        str(background),
        "--product",
        str(product),
        "--x",
        "100",
        "--y",
        "200",
        "--width",
        "300",
        "--out",
        str(output),
    ]
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    image = Image.open(output)
    assert image.size == (800, 1000)
    assert image.mode == "RGBA"
