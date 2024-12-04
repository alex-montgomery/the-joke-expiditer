# src/processors/video_processor.py

import ffmpeg
import logging
from pathlib import Path
from typing import Optional, Dict, Any

class VideoProcessor:
    """
    Handles video processing operations using FFmpeg, specifically optimized for WhatsApp compatibility.
    
    WhatsApp has specific requirements for videos:
    - Recommended maximum size: 16MB
    - Maximum duration: 3 minutes
    - Supported format: MP4 with H.264 video codec and AAC audio codec
    - Typical resolution: 640x640 to 1280x720
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Default FFmpeg parameters optimized for WhatsApp
        self.default_params = {
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'preset': 'medium',  # Balanced between quality and processing time
            'crf': 23,  # Constant Rate Factor - lower means better quality
            'audio_bitrate': '128k',
            'max_size': 16_000_000,  # 16MB in bytes
            'max_duration': 180,  # 3 minutes in seconds
        }
    
    def get_video_info(self, input_path: Path) -> Dict[str, Any]:
        """
        Get information about the input video file.
        Returns dictionary with duration, bitrate, resolution, etc.
        """
        try:
            probe = ffmpeg.probe(str(input_path))
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            return {
                'duration': float(probe['format']['duration']),
                'size': int(probe['format']['size']),
                'bitrate': int(probe['format']['bit_rate']),
                'width': int(video_info['width']),
                'height': int(video_info['height']),
                'codec': video_info['codec_name']
            }
        except Exception as e:
            self.logger.error(f"Error probing video file: {e}")
            raise
    
    def process_for_whatsapp(
        self,
        input_path: Path,
        output_path: Path,
        max_size: Optional[int] = None,
        **kwargs
    ) -> Path:
        """
        Process a video file to make it WhatsApp compatible.
        
        Args:
            input_path: Path to input video file
            output_path: Path to save processed video
            max_size: Maximum file size in bytes (default: 16MB)
            **kwargs: Additional FFmpeg parameters to override defaults
        
        Returns:
            Path to the processed video file
        """
        try:
            # Get input video information
            info = self.get_video_info(input_path)
            
            # Determine if we need to process the video
            if self._is_whatsapp_compatible(info):
                self.logger.info("Video is already WhatsApp compatible")
                return input_path
            
            # Prepare FFmpeg parameters
            params = self.default_params.copy()
            params.update(kwargs)
            max_size = max_size or params['max_size']
            
            # Calculate target bitrate if needed
            if info['size'] > max_size:
                target_bitrate = self._calculate_target_bitrate(info['duration'], max_size)
                params['videoBitrate'] = target_bitrate
            
            # Build FFmpeg command
            stream = ffmpeg.input(str(input_path))
            
            # Video processing
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec=params['audio_codec'],
                vcodec=params['video_codec'],
                audio_bitrate=params['audio_bitrate'],
                preset=params['preset'],
                crf=params['crf'],
                **({'b:v': params['videoBitrate']} if 'videoBitrate' in params else {})
            )
            
            # Run FFmpeg
            self.logger.info(f"Processing video: {input_path.name}")
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            
            # Verify the output
            if not output_path.exists():
                raise FileNotFoundError(f"Failed to create output file: {output_path}")
            
            processed_info = self.get_video_info(output_path)
            self.logger.info(
                f"Processed video stats: "
                f"Size: {processed_info['size'] / 1_000_000:.2f}MB, "
                f"Duration: {processed_info['duration']:.1f}s, "
                f"Resolution: {processed_info['width']}x{processed_info['height']}"
            )
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error processing video: {e}")
            if output_path.exists():
                output_path.unlink()  # Clean up failed output
            raise
    
    def _is_whatsapp_compatible(self, info: Dict[str, Any]) -> bool:
        """Check if video already meets WhatsApp requirements."""
        return (
            info['size'] < self.default_params['max_size'] and
            info['duration'] < self.default_params['max_duration'] and
            info['codec'] == 'h264' and
            info['width'] <= 1280 and
            info['height'] <= 720
        )
    
    def _calculate_target_bitrate(self, duration: float, max_size: int) -> str:
        """Calculate target video bitrate to achieve desired file size."""
        # Account for audio bitrate and container overhead
        audio_size = int(self.default_params['audio_bitrate'].rstrip('k')) * 1000 * duration / 8
        available_size = max_size - audio_size
        # Convert to kb/s and add 10% overhead for container
        target_bitrate = int((available_size * 8 / duration) * 0.9 / 1000)
        return f"{target_bitrate}k"

# Helper function for easy access
def convert_for_whatsapp(input_path: Path, output_path: Path, **kwargs) -> Path:
    """Convenience function to convert a video for WhatsApp."""
    processor = VideoProcessor()
    return processor.process_for_whatsapp(input_path, output_path, **kwargs)