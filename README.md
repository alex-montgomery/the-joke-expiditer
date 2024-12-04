# The Joke Expediter

The Joke Expediter is a powerful tool designed to download videos from various social media platforms and automatically convert them into WhatsApp-compatible format. It supports YouTube, TikTok, and Instagram, handling all the complexities of different video formats and ensuring the output meets WhatsApp's requirements.

## Features

This tool provides seamless video processing with these key features:
- Multi-platform support (YouTube, TikTok, Instagram)
- Automatic WhatsApp optimization
- Secure credential management
- Progress tracking with visual feedback
- Automated cleanup of temporary files
- Smart video format detection and conversion

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

1. Python 3.8 or higher
2. FFmpeg (required for video processing)

### Installing FFmpeg

Choose your operating system and follow the corresponding instructions:

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

## Installation

Follow these steps to set up the project:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/the-joke-expediter.git
cd the-joke-expediter
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate it on macOS/Linux
source venv/bin/activate

# Or on Windows
.\venv\Scripts\activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Run the repository setup script:
```bash
python setup_repo.py
```

## Instagram Authentication Setup

To download from Instagram, you'll need to set up authentication. This only needs to be done once (or when your session expires, typically after 90 days):

1. Install the Cookie-Editor extension for your browser:
   - [Chrome Extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - [Firefox Add-on](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)

2. Log into Instagram in your browser

3. Click the Cookie-Editor extension icon

4. Click "Export" -> "Netscape HTTP Cookie File"

5. Save the content to a temporary file (e.g., `~/Downloads/instagram_cookies.txt`)

6. Run the cookie setup script:
```bash
python -m src.utils.cookie_manager
```

7. When prompted, provide the path to your temporary cookie file

8. After successful setup, you can delete the temporary cookie file

## Usage

The basic command structure is:
```bash
python -m src.main "VIDEO_URL"
```

Examples for different platforms:
```bash
# YouTube video
python -m src.main "https://www.youtube.com/watch?v=dXLCHvRsgRQ"

# TikTok video
python -m src.main "https://www.tiktok.com/@username/video/1234567890"

# Instagram post
python -m src.main "https://www.instagram.com/p/ABC123/"
```

Optional flags:
```bash
# Keep the original downloaded file
python -m src.main --keep-original "VIDEO_URL"
```

## Output

Processed videos are saved in the `output` directory with the following naming convention:
```
output/[platform]_[timestamp]_whatsapp.mp4
```

For example:
```
output/youtube_20240304_144500_whatsapp.mp4
```

# Project Structure

The repository is organized to separate core functionality, configuration, and temporary storage. Here's a detailed breakdown of the directory structure:

```
the-joke-expediter/
├── src/                   # Main source code directory
│   ├── downloaders/       # Platform-specific video downloaders
│   ├── processors/        # Video processing and conversion utilities
│   └── utils/            # Helper functions and utilities
├── config/               # Configuration files and settings
├── downloads/            # Temporary storage for downloaded videos
├── logs/                # Application logs
├── output/              # Processed videos ready for WhatsApp
└── tests/               # Test directory
    ├── integration/     # Integration tests
    └── unit/           # Unit tests
```

Let me explain the purpose of each directory:

The `src` directory contains all the main application code:
- `downloaders`: Contains specialized modules for each platform (YouTube, TikTok, Instagram)
- `processors`: Houses video processing logic, including FFmpeg integration
- `utils`: Includes helper functions like cookie management and authentication

The support directories serve specific purposes:
- `config`: Stores configuration files and any necessary credentials
- `downloads`: Temporary storage for videos during processing (automatically cleaned)
- `output`: Final destination for WhatsApp-ready videos
- `logs`: Contains application logs for troubleshooting

During operation, the application will:
1. Download videos to the `downloads` directory
2. Process them using the video processor
3. Save the final WhatsApp-compatible videos to the `output` directory
4. Maintain logs in the `logs` directory for debugging

The application automatically creates these directories as needed, so you don't need to set them up manually. All temporary files in the `downloads` directory are cleaned up after processing unless you specifically request to keep them using the `--keep-original` flag.

# Video Processing Features

The Joke Expediter intelligently processes videos to ensure WhatsApp compatibility while maintaining the best possible quality. Here's what it does:

## Automatic Size Optimization
- Automatically detects if a video needs compression for WhatsApp (16MB limit)
- Preserves original quality when possible
- Uses smart compression only when necessary
- Maintains aspect ratio during any resizing

## Platform Support
- YouTube videos and shorts
- TikTok videos
- Instagram posts, reels, and stories

## Video Processing Capabilities
- Converts videos to WhatsApp-compatible formats
- Optimizes video codec (H.264) and audio codec (AAC)
- Maintains quality for videos already under size limits
- Progressive compression when size reduction is needed:
  1. High quality (720p)
  2. Medium quality (480p)
  3. Low quality (360p)
  4. Minimum quality (270p) as last resort

## Command Line Options
```bash
# Basic usage
python -m src.main "VIDEO_URL"

# Disable compression (only use if you're sure about file size)
python -m src.main --no-compress "VIDEO_URL"

# Keep original downloaded file
python -m src.main --keep-original "VIDEO_URL"
```

## System Requirements
- Python 3.8 or higher
- FFmpeg (version 4.0 or higher recommended)
- At least 2GB of free disk space for processing
- Active internet connection for video downloads

## Performance Notes
- Processing time depends on video length and original quality
- Temporary files are automatically cleaned up
- Progress bars show download and processing status
- Detailed logging available for troubleshooting

## Supported Video Formats
Input formats: MP4, WebM, MKV, MOV (and others supported by FFmpeg)
Output format: MP4 (optimized for WhatsApp)

## WhatsApp Compatibility
All processed videos are optimized to meet WhatsApp's requirements:
- Maximum file size: 16MB
- Compatible codec: H.264 video, AAC audio
- Supported resolutions: up to 1280x720
- Duration: Unlimited (as long as final size is under 16MB)

## Troubleshooting

1. **FFmpeg errors**: Ensure FFmpeg is properly installed on your system. You can verify by running:
```bash
ffmpeg -version
```

2. **Instagram authentication issues**: If you encounter Instagram download failures, your session might have expired. Simply repeat the Instagram Authentication Setup steps.

3. **File size issues**: WhatsApp has a 16MB limit for videos. The tool automatically optimizes videos to fit within this limit, but extremely long or high-quality videos might result in reduced quality to meet the size requirement.

