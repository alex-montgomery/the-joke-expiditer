#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import json

def create_directory_structure(base_path: str) -> None:
    """Create a standardized directory structure for the video processing tool."""
    
    # Define the directory structure
    directories = [
        "src",
        "src/downloaders",  # Different video platform downloaders
        "src/processors",   # Video processing utilities
        "src/utils",        # Helper functions
        "tests",
        "tests/unit",
        "tests/integration",
        "config",           # Configuration files
        "downloads",        # Temporary storage for downloads
        "output",          # Processed videos
        "logs"             # Application logs
    ]
    
    # Create directories
    for dir_path in directories:
        full_path = os.path.join(base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)
        # Create __init__.py files in Python package directories
        if dir_path.startswith("src") or dir_path.startswith("tests"):
            init_file = os.path.join(full_path, "__init__.py")
            Path(init_file).touch()

    # Create essential files
    files = {
        "README.md": """# The Joke Expediter

A tool for downloading and converting videos to WhatsApp-compatible format.

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m src.main <video_url>
```
""",
        "requirements.txt": """# Core dependencies
requests>=2.26.0
ffmpeg-python>=0.2.0
python-dotenv>=0.19.0
tqdm>=4.62.0

# Development dependencies
pytest>=6.2.5
black>=21.7b0
flake8>=3.9.0
""",
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
.env

# IDE
.idea/
.vscode/

# Project specific
downloads/
output/
logs/
*.mp4
""",
        "src/main.py": """#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='Download and convert videos for WhatsApp')
    parser.add_argument('url', help='URL of the video to process')
    parser.add_argument('--output', '-o', help='Output file name', default=None)
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Processing video from: {args.url}")

if __name__ == "__main__":
    main()
""",
        "config/default_config.json": """{
    "download_path": "downloads",
    "output_path": "output",
    "ffmpeg": {
        "video_codec": "libx264",
        "audio_codec": "aac",
        "preset": "medium",
        "crf": 23,
        "audio_bitrate": "128k"
    }
}"""
    }

    # Create files
    for file_path, content in files.items():
        full_path = os.path.join(base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Skip if file already exists
        if os.path.exists(full_path):
            print(f"Skipping existing file: {file_path}")
            continue
            
        with open(full_path, "w") as f:
            f.write(content)

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.getcwd()
    
    print(f"Creating directory structure in: {base_path}")
    create_directory_structure(base_path)
    print("Repository structure created successfully!")
    print("\nNext steps:")
    print("1. Create a virtual environment: python -m venv venv")
    print("2. Activate the virtual environment:")
    print("   - Windows: .\\venv\\Scripts\\activate")
    print("   - Unix/MacOS: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start developing in src/main.py")

if __name__ == "__main__":
    main()