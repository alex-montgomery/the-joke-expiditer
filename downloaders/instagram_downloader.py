# src/downloaders/instagram_downloader.py

import re
from pathlib import Path
from yt_dlp import YoutubeDL
from .base_downloader import BaseDownloader

class InstagramDownloader(BaseDownloader):
    def __init__(self):
        super().__init__()
        self.ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Instagram often requires authentication
            # Cookies will be loaded from keyring at runtime
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
        }
    
    def is_valid_url(self, url: str) -> bool:
        patterns = [
            r'^https?:\/\/(?:www\.)?instagram\.com\/(?:p|tv)\/[\w-]+',
            r'^https?:\/\/(?:www\.)?instagram\.com\/stories\/[\w\.]+\/\d+',
            r'^https?:\/\/(?:www\.)?instagram\.com\/(?:[\w\.]+\/)?reel\/[\w-]+\/?'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def extract_video_id(self, url: str) -> str:
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid Instagram URL: {url}")
            
        # Extract the shortcode from the URL
        match = re.search(r'(?:p|reel|tv)\/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
            
        # Handle stories differently
        match = re.search(r'stories\/[\w\.]+\/(\d+)', url)
        if match:
            return f"story_{match.group(1)}"
            
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def download(self, url: str, output_path: Path) -> Path:
        try:
            video_id = self.extract_video_id(url)
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            
            output_file = output_path / f"instagram_{video_id}.mp4"
            self.ydl_opts['outtmpl'] = str(output_file)
            
            # Load cookies from keyring
            from src.utils.cookie_manager import InstagramCookieManager
            cookie_manager = InstagramCookieManager()
            cookies = cookie_manager.get_cookies_from_keyring()
            
            if not cookies:
                self.logger.error("No Instagram cookies found in keyring. Run python -m src.utils.cookie_manager to set them up.")
                raise ValueError("Instagram authentication required")
                
            self.ydl_opts['cookies'] = cookies  # Pass cookies directly to yt-dlp
            
            self.logger.info(f"Downloading Instagram video: {video_id}")
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
                
            if not output_file.exists():
                raise FileNotFoundError(f"Download failed: {url}")
                
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error downloading Instagram video: {str(e)}")
            raise