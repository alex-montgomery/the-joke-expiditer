#!/usr/bin/env python3
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
