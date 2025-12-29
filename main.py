import os
import subprocess
from tqdm import tqdm

from config import *
from audio_utils import extract_audio_peaks
from scene_utils import detect_scenes
from text_utils import transcribe
from video_utils import cut_clip,burn_subs, extract_frame,cut_short_with_fx,cut_clip_with_fx
from text_utils import transcribe_clip, generate_title, transcribe_segments,generate_shorts_title
from subs_utils import make_ass
from thumb_utils import make_thumbnail
from get_eng_aud_idx import get_eng_audio_index
os.makedirs(WORKDIR, exist_ok=True)
AUDIO_PATH = os.path.join(WORKDIR, "audio.wav")


def overlap_sec(a, b):
    return max(0, min(a[2], b[2]) - max(a[1], b[1]))
def crop(VIDEO_PATH):
    print("[1] Извлекаю аудио")
    aud_idx = get_eng_audio_index(VIDEO_PATH,LANG)
    result_fx =subprocess.run([
        "ffmpeg", "-y", "-i", VIDEO_PATH, "-map", f"0:{aud_idx}","-vn",
        "-ac", "1", "-ar", "22050", AUDIO_PATH
    ], capture_output=True, text=True)
    if result_fx.returncode != 0:
            print("[ERROR] extract audio failed:", result_fx.stderr)
    else:
        print("[OK] Audio extracted:", AUDIO_PATH)
    print("[2] Детект сцен")
    scenes = detect_scenes(VIDEO_PATH)

    print("[3] Анализ аудио")
    audio_peaks = extract_audio_peaks(AUDIO_PATH)

    print("[4] Формирую Shorts-кандидаты")
    shorts = []
    final_shorts = []
    for t, e in audio_peaks:
        if t < SKIP_START_SECONDS:
            continue
        score = e * 3.3
        start = max(t - SHORTS_PRE, SKIP_START_SECONDS)
        end = start + SHORTS_LEN

        shorts.append((score, start, end))
    shorts.sort(reverse=True)
    for s in shorts:
        if all(overlap_sec(s, f) < 8 for f in final_shorts):
            final_shorts.append(s)
        if len(final_shorts) == SHORTS_TOP_K:
            break

    print("[5] Нарезаю Shorts")
    for i, (score, start, end) in enumerate(final_shorts):
        try:
            video_name = os.path.splitext(os.path.basename(VIDEO_PATH))[0]
            path = f"{WORKDIR}/short_{video_name}_{i+1:02d}.mp4"
            print(start,end)
            cut_short_with_fx(
                VIDEO_PATH,
                start,
                end,
                path
            )
            text = transcribe_clip(path)
            title = generate_shorts_title(text)
            

            with open(f"{WORKDIR}/{video_name}_short_{i+1:02d}.txt", "w", encoding="utf-8") as f:
                f.write(title + "\n\n" + text)
            print(f"Shorts {i+1}: {title}")
            segments = transcribe_segments(path)
            ass_path = path.replace(".mp4", ".ass")
            make_ass(segments, ass_path, vertical=True)
            subbed = path.replace(".mp4", "_sub.mp4")
            burn_subs(path, ass_path, subbed)
            # thumb_frame = path.replace(".mp4", "_frame.jpg")
            # thumb_out = path.replace(".mp4", "_thumb.jpg")
            # if segments:
                # extract_frame(path, segments[0][0], thumb_frame)
            # else:
                # extract_frame(path, SHORTS_PRE, thumb_frame)
            # make_thumbnail(thumb_frame, title, thumb_out)
        except Exception as e:
            print(e)




if __name__=="__main__":
    folder = "F:/Simpsons"
    videos = [
        os.path.abspath(os.path.join(folder, f))
        for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS
    ]
    for v in videos:
        try:
            print(v)
            crop(v)
        except Exception as e:
            print(e)