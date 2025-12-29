from faster_whisper import WhisperModel
import re
import subprocess
import os

EMO_WORDS = [
    "нет", "да", "черт", "убью", "люблю", "ненавижу",
    "пожалуйста", "стой", "боже", "помоги"
]
model = WhisperModel("medium", compute_type="int8")

def text_emotion_score(text):
    score = 0
    for w in EMO_WORDS:
        if w in text.lower():
            score += 1
    score += len(re.findall(r"[!?.]{2,}", text))
    return score


def transcribe(audio_path, model_name="medium"):
    model = WhisperModel(model_name, compute_type="int8")
    segments, _ = model.transcribe(audio_path)

    result = []
    for seg in segments:
        score = text_emotion_score(seg.text)
        result.append((seg.start, seg.end, score))

    return result


def extract_audio(video_path, wav_path):
    os.makedirs(os.path.dirname(wav_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",

        wav_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0 or not os.path.exists(wav_path):
        print(f"[ERROR] Не удалось создать WAV: {wav_path}")
        print(result.stderr)
    else:
        print(f"[OK] WAV создан: {wav_path}")

def transcribe_clip(video_path):
    wav = video_path.replace(".mp4", ".wav")
    extract_audio(video_path, wav)

    if not os.path.exists(wav):
        return ""
    segments, _ = model.transcribe(wav)
    text = " ".join(seg.text.strip() for seg in segments)
    return text



def generate_title(text):
    text = text.strip()
    if not text:
        return "Эмоциональный момент"
    text = re.sub(r"\s+", " ", text)
    candidates = re.split(r"[.!?]", text)
    candidates = [c.strip() for c in candidates if len(c.strip()) > 10]
    base = candidates[0] if candidates else text[:80]
    hooks = [
        "— и всё изменилось",
        "… и дальше было неожиданно",
        "— реакция шокирует",
        "— никто не ожидал этого"
    ]

    return (base[:80] + " " + hooks[hash(base) % len(hooks)]).strip()
def generate_shorts_title(text):
    hook = "#films #triller #crop #нарезка"
    text = text.strip().replace("\n", " ")
    parts = text.split(".")
    base = parts[0][:57]+"..." if parts else text[:57]+"..."
    return base + " " + hook
def transcribe_segments(video_path):
    wav = video_path.replace(".mp4", ".wav")
    extract_audio(video_path, wav)
    segments, _ = model.transcribe(wav)
    return [
        (seg.start, seg.end, seg.text.strip())
        for seg in segments
        if seg.text.strip()
    ]
