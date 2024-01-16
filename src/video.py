import os
import json
from googleapiclient.discovery import build


class Video:

    def __init__(self, video):
        """Инициализируем класс по id видео, также инициализируем
        название, количество просмотров и лайков"""
        api_key: str = os.getenv('YouTube_API_Key')
        youtube = build('youtube', 'v3', developerKey=api_key)

        try:
            self.video = youtube.videos().list(id=video, part='snippet,contentDetails,statistics').execute()
            self.video_id = self.video["items"][0]["id"]
            self.video_title = self.video["items"][0]["snippet"]["title"]
            self.video_views = self.video["items"][0]["statistics"]["viewCount"]
            self.video_likes = self.video["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.video = video
            self.video_id = None
            self.video_title = None
            self.video_views = None
            self.video_likes = None

    def __repr__(self):
        """Получаем название канала в формате Youtube-канал: <название_канала>"""
        return f"Youtube-канал: {self.video_title}"

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video, playlist):
        """Инициализируем дочерний класс по id видео, и id плейлиста"""
        super().__init__(video)
        api_key: str = os.getenv('YouTube_API_Key')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = playlist
        self.playlist_name = self.get_playlist_name()

    def get_playlist_name(self):
        """Получаем название плейлиста"""
        self.playlist = self.youtube.playlists().list(id=self.playlist, part='snippet').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']
        return self.playlist_name

    def __repr__(self):
        """Переопределили метод репр в дочернем классе"""
        return f"{self.video_title} ({self.playlist_name})"
