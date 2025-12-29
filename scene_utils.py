from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

def detect_scenes(video_path):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=27))
    scene_manager.detect_scenes(video)

    scenes = []
    for start, end in scene_manager.get_scene_list():
        scenes.append((start.get_seconds(), end.get_seconds()))
    return scenes
