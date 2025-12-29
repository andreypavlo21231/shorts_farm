import subprocess
import os
from get_eng_aud_idx import get_eng_audio_index
from config import *
def cut_clip_with_fx(
    
    video_path,
    start,
    end,
    out_path,
    zoom_start=0.9,
    zoom_end=1.0
):
    duration = end - start
    aud_idx = get_eng_audio_index(video_path,LANG)
    zoom_expr = (
        f"zoompan=z='if(between(t,{duration*0.3},{duration*0.6}),"
        f"{zoom_start}+({zoom_end-zoom_start})*(t-{duration*0.3})/{duration*0.3},"
        f"{zoom_start})':d=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", video_path,
        "-vf", zoom_expr,
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-map", f"0:{aud_idx}","-vn",
        out_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import ffmpeg
import os

def cut_clip(video_path, start, end, out_path):
    (
        ffmpeg
        .input(video_path, ss=start, to=end)
        .output(out_path, c="copy")
        .overwrite_output()
        .run(quiet=True)
    )
def cut_short_with_fx(video_path, start, end, out_path):
    aud_idx = get_eng_audio_index(video_path,LANG)
    duration = end - start
    temp_clip = out_path.replace(".mp4", "_tmp.mp4")
    # subprocess.run([
        # "ffmpeg", "-y",
        # "-ss", str(start),
        # "-t", str(duration),
        # "-i", video_path,
        # "-c", "copy",
        # temp_clip
    # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", video_path,

        "-map", "0:v:0",
        "-map", f"0:{aud_idx}",

        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",

        "-c:a", "aac",
        "-ac", "2",

        temp_clip
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    vf = "crop=in_h*9/16:in_h,scale=1080:1920"
    cmd_fx = [
        "ffmpeg", "-y",
        
        "-i", temp_clip,
        
        "-map", "0:v:0",
        "-map", "0:a:0",

        "-vf", vf,
        # 🔥 УБРАЛ pan — он больше не нужен
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",

        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",

        "-c:a", "aac",
        "-b:a", "128k",

        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",

        out_path
]

    result_fx = subprocess.run(cmd_fx, capture_output=True, text=True)
    if result_fx.returncode != 0:
        print("[ERROR] cut_short_with_fx failed:", result_fx.stderr)
    else:
        print("[OK] Short created:", out_path)

    if os.path.exists(temp_clip):
        os.remove(temp_clip)


def burn_subs(video_path, subs_path, out_path):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"ass={subs_path}",
        "-c:a", "copy",
        out_path
    ]
    result_fx = subprocess.run(cmd, capture_output=True, text=True)
    if result_fx.returncode != 0:
        print("[ERROR] burn_subs failed:", result_fx.stderr)
    else:
        print("[OK] subs burned:", out_path)


def extract_frame(video_path, t, out_path):
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(t),
        "-i", video_path,
        "-frames:v", "1",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if __name__=="__main__":
    cut_short_with_fx("F:/Simpsons/1.mkv",894,933,'1.mp4')