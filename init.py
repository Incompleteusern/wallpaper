from pathlib import Path

source_dir = Path(__file__).resolve().parent

import os

os.makedirs(os.path.join(source_dir, "wallpapers"))

for i in ["Clear", "Snow", "Rain", "Clouds"]:
    for j in ["Morning", "Noon", "Night", "Evening"]:
            os.makedirs(os.path.join(source_dir, "wallpapers", i, j))
