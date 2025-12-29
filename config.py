# VIDEO_PATH = "F:/Simpsons/1.mkv"
WORKDIR = "output"

CLIP_MIN_LEN = 47     # секунд
CLIP_MAX_LEN = 60
SKIP_START_SECONDS = 600      # первые 10 минут пропускаются
CLIP_TARGET_LEN = 55         # оптимум для удержания
PRE_ROLL = 8                 # секунд до пика
POST_ROLL = 47               # после пика
FINAL_TOP_K = 12          
# Shorts
SHORTS_LEN = 39
SHORTS_PRE = 4.5      # до пика
SHORTS_POST = 34.5    # после
SHORTS_TOP_K = 15

AUDIO_PEAK_THRESHOLD = 0.75
FINAL_TOP_K = 10     # сколько клипов сохранить

WHISPER_MODEL = "medium"
VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv",
    ".webm", ".mpeg", ".mpg", ".m4v", ".3gp"
}
LANG='eng'