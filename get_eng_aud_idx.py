import subprocess
import os
import json

def get_eng_audio_index(video_path,LANG):
    p = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=index:stream_tags=language",
            "-of", "json",
            "-i", video_path
        ],
        capture_output=True, text=True
    )
    data = json.loads(p.stdout)
    print(data)
    for s in data.get("streams", []):
    
        if s.get("tags", {}).get("language") == LANG:
            return s["index"]
    return 0  # fallback
if __name__=="__main__":
    print(get_eng_audio_index('movie.mkv'))