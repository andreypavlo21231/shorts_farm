import re

def make_ass(segments, out_path, vertical=True):
    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        return f"{h}:{m:02}:{s:05.2f}"

    play_res_y = 1920 if vertical else 1080
    font_size = 79 if vertical else 44
    margin_v = int(play_res_y * 0.275)
    margin_lr = 80

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: {play_res_y}
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,{font_size},&H00FFFFFF,&H00000000,&H64000000,1,0,1,4,1,2,{margin_lr},{margin_lr},{margin_v},1

[Events]
Format: Layer,Start,End,Style,Text
""")

        for start, end, text in segments:
            duration = end - start
            words = re.findall(r"\w+['’]?\w*|[.,!?]", text)

            if not words:
                continue
            k = max(1, int(duration * 100 / len(words)))
            karaoke = ""
            for w in words:
                karaoke += f"{{\\k{k}}}{w} "
            f.write(
                f"Dialogue: 0,{ts(start)},{ts(end)},Default,{karaoke.strip()}\n"
            )
