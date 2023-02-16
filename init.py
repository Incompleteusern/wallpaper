
import os

for i in ["Clear", "Snow", "Rain", "Clouds"]:
    for j in ["Morning", "Noon", "Night", "Evening"]:
            os.makedirs(os.path.join(source_dir, "wallpapers", i, j))
