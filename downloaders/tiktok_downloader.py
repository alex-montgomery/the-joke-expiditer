# src/downloaders/tiktok_downloader.py

import re
from pathlib import Path
from yt_dlp import YoutubeDL
from .base_downloader import BaseDownloader

class TikTokDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            # Additional cookies or headers might be needed for TikTok
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
    
    def is_valid_url(self, url: str) -> bool:
        patterns = [
            r'^https?:\/\/(?:www\.)?tiktok\.com\/@[\w.-]+\/video\/\d+',
            r'^https?:\/\/(?:vm|vt)\.tiktok\.com\/\w+',
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def extract_video_id(self, url: str) -> str:
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid TikTok URL: {url}")
            
        # Handle shortened URLs first
        if 'vm.tiktok.com' in url or 'vt.tiktok.com' in url:
            # We'll need to follow redirects to get the actual URL
            # This will be implemented in the download method
            return url
            
        match = re.search(r'video\/(\d+)', url)
        if match:
            return match.group(1)
            
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def download(self, url: str, output_path: Path) -> Path:
        try:
            video_id = self.extract_video_id(url)
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            
            output_file = output_path / f"tiktok_{video_id}.mp4"
            self.ydl_opts['outtmpl'] = str(output_file)
            
            self.logger.info(f"Downloading TikTok video: {url}")
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
                
            if not output_file.exists():
                raise FileNotFoundError(f"Download failed: {url}")
                
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error downloading TikTok video: {str(e)}")
            raise