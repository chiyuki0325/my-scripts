from pathlib import Path as P
from xml.etree import ElementTree as ET
import subprocess as sp
import UnityPy

CONVERTER = "/home/chiyuki/应用/MaichartConverter/bin/Debug/net8.0/linux-x64/MaichartConverter"
CRI_TOOLS = "/home/chiyuki/应用/CriTools/src/index.js"
KEY = "9170825592834449000"
A000 = P("/run/media/chiyuki/SDGA/prism/option/A011/")
A000_FALLBACK = P("/run/media/chiyuki/SDGA/prism/Sinmai_Data/StreamingAssets/A000/")
VERSION = 23
VERSION_NAME = "maimai DX PRiSM"
OUPUT_DIR = P("pria004")

LEVEL_MAP = {
    24: "15+",
    23: "15",
    22: "14+",
    21: "14",
    20: "13+",
    19: "13",
    18: "12+",
    17: "12",
    16: "11+",
    15: "11",
    14: "10+",
    13: "10",
    12: "9+",
    11: "9",
    10: "8+",
    9: "8",
    8: "7+",
    7: "7",
    6: "6",
    5: "5",
    4: "4",
    3: "3",
    2: "2",
    1: "1",
    0: "0",
}

GENRE = {
    '101': 'POPSアニメ',
    '102': 'niconicoボーカロイド',
    '103': '東方Project',
    '104': 'ゲームバラエティ',
    '105': 'maimai',
    '106': 'オンゲキCHUNITHM',
    '107': '宴会場'
}

def strip_maidata(maidata: str) -> str:
    lines = []
    started = False
    for line in maidata.split("\n"):
        if line.startswith("("):
            started = True
        if started:
            lines.append(line)
    return "\n".join(lines).strip()

for music_dir in (A000 / "music").iterdir():
    if music_dir.is_dir():
        xml = music_dir / "Music.xml"
        if not xml.exists():
            continue
        tree = ET.parse(xml)
        ver = int(tree.find("AddVersion").find("id").text)
        if ver != VERSION:
            continue
        song_id = int(tree.find("name").find("id").text)
        if song_id > 100000:
            continue
        dx =  song_id >= 10000

        title = tree.find("name").find("str").text
        print(f"[{song_id}] {title}")

        sort_name = tree.find("sortName").text
        # genre = tree.find("genreName").find("str").text
        genre= GENRE[tree.find("genreName").find("id").text]
        
        conv_dir = OUPUT_DIR / genre / f"{song_id}_{sort_name}{'_DX' if dx else ''}"
        conv_dir.mkdir(parents=True, exist_ok=True)

        bpm = tree.find("bpm").text
        artist = tree.find("artistName").find("str").text
        artist_id = tree.find("artistName").find("id").text
        genre_id = tree.find("genreName").find("id").text

        des = {}
        lv = {}
        for notes in tree.find("notesData").iter("Notes"):
            ma2_path = notes.find("file").find("path").text
            diff_id = int(ma2_path[-5])
            des[diff_id] = notes.find("notesDesigner").find("str").text
            lv[diff_id] = LEVEL_MAP[int(notes.find("musicLevelID").text)]

        maidata = str(
            f"&title={title} {'[DX]' if dx else '[SD]'}\n"
            f"&wholebpm={bpm}\n"
            f"&artist={artist}\n"
            f"&artistid={artist_id}\n"
            f"&des={des[3]}\n"
            f"&shortid={song_id}\n"
            f"&genre={genre}\n"
            f"&genreid={genre_id}\n"
            f"&cabinet={'DX' if dx else 'SD'}\n"
            f"&version={VERSION_NAME}\n\n"
        )

        # print(des,lv)

        for diff in [0,1,2,3,4]:
            maidata_diff = diff+2
            # 0 1 2 3 4 -> 2 3 4 5 6
            if diff not in lv:
                continue
            if lv[diff]=="0":
                # 谱面不存在
                continue
            # id pad 到六位数，diff pad 到两位数
            ma2_path = music_dir / f"{song_id:06}_{diff:02}.ma2"
            if not ma2_path.exists():
                continue
            proc = sp.run([CONVERTER, "CompileMa2", "-p", str(ma2_path)], capture_output=True)
            if proc.returncode != 0:
                print(proc.stderr.decode())
                continue

            print(f"  [{diff}] {lv[diff]} {des[diff]}")

            maidata += str(
                f"&lv_{maidata_diff}={lv[diff]}\n"
                f"&des_{maidata_diff}={des[diff] if des[diff] else '-'}\n"
                f"&inote_{maidata_diff}=\n"
                f"{strip_maidata(proc.stdout.decode())}\n\n"
            )
        
        # maidata 完毕
        with open(conv_dir / "maidata.txt", "w") as f:
            f.write(maidata)

        png_jacket_path = A000 / "AssetBundleImages" / "jacket" / f"ui_jacket_{(song_id%10000):06}.png"
        if png_jacket_path.exists():
            # 已经转换好封面
            sp.run(["magick", str(png_jacket_path), str(conv_dir / "bg.jpg")])
            print("  [Jacket] PNG")
        else:
            for ab_jacket_path in [
                A000 / "AssetBundleImages" / "jacket" / f"ui_jacket_{(song_id%10000):06}.ab",
                A000_FALLBACK / "AssetBundleImages" / "jacket" / f"ui_jacket_{(song_id%10000):06}.ab",
            ]:
                if ab_jacket_path.exists():
                    temp = P(f"/tmp/{song_id}.png")
                    unity = UnityPy.load(open(ab_jacket_path, 'rb'))
                    for obj in unity.objects:
                        if obj.type.name == 'Sprite':
                            obj.read().image.save(temp)
                            break
                    sp.run(["magick", str(temp), str(conv_dir / "bg.jpg")])
                    print("  [Jacket] AssetsBundle")
                    temp.unlink()
                    break
                
        # jacket 完毕

        # 音频
        for acb_path in [
            A000 / "SoundData" / f"music{(song_id%10000):06}.acb",
            A000_FALLBACK / "SoundData" / f"music{(song_id%10000):06}.acb",
        ]:
            if acb_path.exists():
                proc = sp.run(["node", CRI_TOOLS, "acb2wavs", "-k", KEY, "-o", f"/tmp/{song_id}", str(acb_path)], capture_output=True)
                # 有时候 awb 的名字可能和 acb 的名字不一样导致工具退出
                stderr = proc.stderr.decode()
                if 'ERROR' in stderr:
                    awb = stderr.split(" ")[-1].strip()
                    print(f"  [Music] Moved: {awb}")
                    awb_path = acb_path.parent / awb
                    sp.run(["cp", str(acb_path.with_suffix(".awb")), str(awb_path)])
                    proc = sp.run(["node", CRI_TOOLS, "acb2wavs", "-k", KEY, "-o", f"/tmp/{song_id}", str(acb_path)], capture_output=True)
                    awb_path.unlink()
                sp.run(["ffmpeg", "-i", f"/tmp/{song_id}/stream_1.wav", "-c:a", "libmp3lame", "-q:a", "0", str(conv_dir / "track.mp3")], capture_output=True)
                print("  [Music] ACB")
                P(f"/tmp/{song_id}/stream_1.wav").unlink()
                sp.run(["rm", "-r", f"/tmp/{song_id}"])
                break