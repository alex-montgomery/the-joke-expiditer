# src/main.py

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# Import our components
from downloaders.youtube_downloader import YouTubeDownloader
from downloaders.tiktok_downloader import TikTokDownloader
from downloaders.instagram_downloader import InstagramDownloader
from src.processors.video_processor import VideoProcessor

class VideoConverter:
    """Main application class that handles the video conversion workflow."""
    
    def __init__(self):
        # Set up rich console for pretty output
        self.console = Console()
        
        # Initialize our components
        self.youtube = YouTubeDownloader()
        self.tiktok = TikTokDownloader()
        self.instagram = InstagramDownloader()
        self.processor = VideoProcessor()
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[RichHandler(console=self.console, show_time=False)]
        )
        self.logger = logging.getLogger("video_converter")
    
    def _detect_platform(self, url: str) -> tuple[str, Optional[object]]:
        """Determine which platform the URL is from and return appropriate downloader."""
        if self.youtube.is_valid_url(url):
            return "YouTube", self.youtube
        elif self.tiktok.is_valid_url(url):
            return "TikTok", self.tiktok
        elif self.instagram.is_valid_url(url):
            return "Instagram", self.instagram
        else:
            return "Unknown", None
    
    def _generate_output_filename(self, platform: str) -> Path:
        """Generate a unique output filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        return output_dir / f"{platform.lower()}_{timestamp}_whatsapp.mp4"
    
    def process_url(self, url: str, compress: bool = True) -> Optional[Path]:
        """Main workflow to download and process a video from a given URL."""
        try:
            # Detect platform and get appropriate downloader
            platform, downloader = self._detect_platform(url)
            if not downloader:
                self.console.print(f"[red]Error: Unsupported URL format: {url}")
                self.console.print("Supported platforms: YouTube, TikTok, Instagram")
                return None
            
            # Create progress display
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                # Step 1: Download the video
                download_task = progress.add_task(
                    f"[cyan]Downloading {platform} video...",
                    total=None
                )
                
                downloads_dir = Path("downloads")
                downloads_dir.mkdir(exist_ok=True)
                downloaded_file = downloader.download(url, downloads_dir)
                progress.update(download_task, completed=True)
                
                # Step 2: Process for WhatsApp
                process_task = progress.add_task(
                    "[cyan]Converting for WhatsApp...",
                    total=None
                )
                
                output_file = self._generate_output_filename(platform)
                processed_file = self.processor.process_for_whatsapp(
                    downloaded_file,
                    output_file,
                    compress=compress
                )
                progress.update(process_task, completed=True)
                
                # Clean up downloaded file
                if downloaded_file.exists():
                    downloaded_file.unlink()
                
                return processed_file
                
        except Exception as e:
            self.console.print(f"[red]Error processing video: {str(e)}")
            return None

def main():
    """Entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Download and convert videos for WhatsApp compatibility"
    )
    parser.add_argument(
        "url",
        help="URL of the video to process (YouTube, TikTok, or Instagram)"
    )
    parser.add_argument(
        "--keep-original",
        action="store_true",
        help="Keep the original downloaded file"
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Disable automatic compression (may result in files too large for WhatsApp)"
    )
    args = parser.parse_args()
    
    converter = VideoConverter()
    console = Console()
    
    try:
        console.print("\n[bold cyan]🎥 The Joke Expediter[/bold cyan]")
        console.print("Converting video for WhatsApp...\n")
        
        output_file = converter.process_url(args.url, compress=not args.no_compress)
        
        if output_file:
            console.print(
                f"\n[green]✅ Success! Video saved to:[/green] "
                f"[bold white]{output_file}[/bold white]\n"
            )
            
            # Print file size
            size_mb = output_file.stat().st_size / (1024 * 1024)
            console.print(
                f"File size: [bold]{size_mb:.1f}MB[/bold] "
                f"({'[green]WhatsApp ready!' if size_mb <= 16 else '[red]Too large for WhatsApp!'}')"
            )
        else:
            console.print("\n[red]❌ Failed to process video[/red]\n")
            sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main()