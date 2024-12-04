# src/processors/video_processor.py

import ffmpeg
import logging
from pathlib import Path
from typing import Optional, Dict, Any

class VideoProcessor:
    """Handles video processing operations using FFmpeg, optimized for WhatsApp compatibility."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.WHATSAPP_MAX_SIZE = 16_000_000  # 16MB in bytes
    
    def get_video_info(self, input_path: Path) -> Dict[str, Any]:
        """Get information about the input video file."""
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

    def compress_video(self, input_path: Path, output_path: Path) -> Optional[Path]:
        """Attempt to compress video using various quality levels until size requirement is met."""
        compression_attempts = [
            {
                'scale': '1280:720',
                'crf': 23,
                'desc': 'High quality (720p)'
            },
            {
                'scale': '854:480',
                'crf': 28,
                'desc': 'Medium quality (480p)'
            },
            {
                'scale': '640:360',
                'crf': 32,
                'desc': 'Low quality (360p)'
            },
            {
                'scale': '480:270',
                'crf': 35,
                'desc': 'Minimum quality (270p)'
            }
        ]

        for attempt in compression_attempts:
            self.logger.info(f"Trying compression: {attempt['desc']}")
            temp_output = output_path.with_stem(f"{output_path.stem}_temp")

            try:
                # Construct FFmpeg command with explicit compression settings
                stream = (
                    ffmpeg
                    .input(str(input_path))
                    .output(
                        str(temp_output),
                        vf=f"scale={attempt['scale']}:force_original_aspect_ratio=decrease",
                        crf=attempt['crf'],
                        preset='medium',
                        vcodec='libx264',
                        acodec='aac',
                        audio_bitrate='128k',
                        maxrate='2M',
                        bufsize='2M',
                        max_muxing_queue_size=1024
                    )
                    .overwrite_output()
                )

                # Run the compression
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

                if temp_output.exists():
                    compressed_size = temp_output.stat().st_size
                    self.logger.info(f"Compressed size: {compressed_size / 1_000_000:.2f}MB")

                    if compressed_size <= self.WHATSAPP_MAX_SIZE:
                        temp_output.replace(output_path)
                        self.logger.info(f"Successfully compressed using {attempt['desc']}")
                        return output_path

                    temp_output.unlink()
                    self.logger.info("File still too large, trying next compression level")

            except Exception as e:
                self.logger.error(f"Compression attempt failed: {e}")
                if temp_output.exists():
                    temp_output.unlink()

        return None

    def process_for_whatsapp(
        self,
        input_path: Path,
        output_path: Path,
        compress: bool = True
    ) -> Path:
        """Process a video file to make it WhatsApp compatible."""
        try:
            # Get input video information
            info = self.get_video_info(input_path)
            self.logger.info(
                f"Input video stats - Size: {info['size'] / 1_000_000:.2f}MB, "
                f"Duration: {info['duration']:.1f}s, "
                f"Resolution: {info['width']}x{info['height']}"
            )

            # Check if compression is needed
            if info['size'] <= self.WHATSAPP_MAX_SIZE:
                self.logger.info("Video is already under WhatsApp size limit")
                # Still perform basic conversion for codec compatibility
                stream = (
                    ffmpeg
                    .input(str(input_path))
                    .output(
                        str(output_path),
                        vcodec='libx264',
                        acodec='aac',
                        audio_bitrate='128k',
                        crf=23,  # Maintain quality level
                        preset='medium',
                        maxrate='2M',
                        bufsize='2M',
                        # Copy original resolution
                        vf=f"scale={info['width']}:{info['height']}:force_original_aspect_ratio=decrease"
                    )
                    .overwrite_output()
                )
                ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
                return output_path

            if not compress:
                self.logger.warning("Compression disabled but file exceeds WhatsApp limit")
                raise ValueError("File too large for WhatsApp and compression disabled")

            # Attempt compression
            self.logger.info("Video requires compression for WhatsApp compatibility")
            result = self.compress_video(input_path, output_path)
            
            if result is None:
                raise ValueError("Could not compress video to meet WhatsApp size limit")
                
            return result

        except Exception as e:
            self.logger.error(f"Error processing video: {str(e)}")
            if output_path.exists():
                output_path.unlink()
            raise