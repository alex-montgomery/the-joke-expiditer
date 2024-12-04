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

## Project Structure

```
the-joke-expediter/
├── src/
│   ├── downloaders/        # Platform-specific video downloaders
│   ├── processors/         # Video processing utilities
│   └── utils/             # Helper functions
├── downloads/             # Temporary storage for downloads
├── output/               # Processed videos
└── logs/                # Application logs
```

## Troubleshooting

1. **FFmpeg errors**: Ensure FFmpeg is properly installed on your system. You can verify by running:
```bash
ffmpeg -version
```

2. **Instagram authentication issues**: If you encounter Instagram download failures, your session might have expired. Simply repeat the Instagram Authentication Setup steps.

3. **File size issues**: WhatsApp has a 16MB limit for videos. The tool automatically optimizes videos to fit within this limit, but extremely long or high-quality videos might result in reduced quality to meet the size requirement.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.