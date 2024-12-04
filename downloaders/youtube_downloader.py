# src/downloaders/youtube_downloader.py

import re
from pathlib import Path
from yt_dlp import YoutubeDL
from .base_downloader import BaseDownloader

class YouTubeDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
    
    def is_valid_url(self, url: str) -> bool:
        patterns = [
            r'^https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[\w-]+',
            r'^https?:\/\/(?:www\.)?youtube\.com\/shorts\/[\w-]+',
            r'^https?:\/\/youtu\.be\/[\w-]+'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def extract_video_id(self, url: str) -> str:
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid YouTube URL: {url}")
            
        patterns = [
            r'(?:v=|\/)([\w-]{11})(?:\?|&|\/|$)',
            r'(?:shorts\/)([\w-]{11})(?:\?|&|\/|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def download(self, url: str, output_path: Path) -> Path:
        video_id = self.extract_video_id(url)
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = output_path / f"{video_id}.mp4"
        self.ydl_opts['outtmpl'] = str(output_file)
        
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                self.logger.info(f"Downloading YouTube video: {video_id}")
                ydl.download([url])
                
            if not output_file.exists():
                raise FileNotFoundError(f"Download failed: {url}")
                
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error downloading YouTube video: {str(e)}")
            raise