# src/downloaders/base_downloader.py

from abc import ABC, abstractmethod
from pathlib import Path
import logging

class BaseDownloader(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def extract_video_id(self, url: str) -> str:
        """Extract the video ID from the platform-specific URL."""
        pass
    
    @abstractmethod
    def download(self, url: str, output_path: Path) -> Path:
        """Download the video from the given URL.
        
        Args:
            url: The URL of the video to download
            output_path: Directory to save the downloaded video
            
        Returns:
            Path to the downloaded video file
        """
        pass
    
    @abstractmethod
    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid for this platform."""
        pass