from mutagen.flac import FLAC, Picture
from pathlib import Path
import subprocess

for file in Path("/home/yidaozhan/音乐/maimai FESTiVAL OST/").iterdir():
    if file.is_file() and file.suffix == '.flac':
        audio = FLAC(file)
        try:
            picture = audio.pictures[0]
            if picture.mime == "image/png":
                picture_data = picture.data
                png_path = Path("/tmp/qwq") / (file.stem + ".png")
                with open(png_path, 'wb') as f:
                    f.write(picture_data)
                subprocess.run(["convert", png_path, png_path.with_suffix(".jpg")])
                subprocess.run(["rm", png_path])
                picture.mime = "image/jpeg"
                picture.type = 3
                picture.data = png_path.with_suffix(".jpg").read_bytes()
                audio.save()
                subprocess.run(["rm", png_path.with_suffix(".jpg")])
        except IndexError:
            pass