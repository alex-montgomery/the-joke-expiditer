# src/utils/cookie_manager.py

import keyring
import json
import logging
from pathlib import Path
from typing import Dict, Optional

class InstagramCookieManager:
    SERVICE_NAME = "the-joke-expediter"
    COOKIE_KEY = "instagram_cookies"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def save_cookies_to_keyring(self, cookie_file: Path) -> bool:
        """Read cookies from file and save to system keyring."""
        try:
            # Read the Netscape cookie file
            cookies = {}
            with open(cookie_file, 'r') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    fields = line.strip().split('\t')
                    if len(fields) >= 7:
                        cookies[fields[5]] = fields[6]
            
            # Store in keyring as JSON string
            keyring.set_password(
                self.SERVICE_NAME,
                self.COOKIE_KEY,
                json.dumps(cookies)
            )
            
            self.logger.info("Successfully saved cookies to system keyring")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save cookies to keyring: {e}")
            return False
    
    def get_cookies_from_keyring(self) -> Optional[Dict[str, str]]:
        """Retrieve cookies from system keyring."""
        try:
            cookie_data = keyring.get_password(self.SERVICE_NAME, self.COOKIE_KEY)
            if cookie_data:
                return json.loads(cookie_data)
            return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve cookies from keyring: {e}")
            return None
    
    def clear_cookies_from_keyring(self) -> bool:
        """Remove stored cookies from keyring."""
        try:
            keyring.delete_password(self.SERVICE_NAME, self.COOKIE_KEY)
            self.logger.info("Successfully cleared cookies from keyring")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear cookies from keyring: {e}")
            return False

def setup_cookies():
    """Interactive setup for Instagram cookies."""
    import sys
    
    logging.basicConfig(level=logging.INFO)
    manager = InstagramCookieManager()
    
    print("\n=== Instagram Cookie Setup ===")
    
    # Check if cookies already exist
    existing_cookies = manager.get_cookies_from_keyring()
    if existing_cookies:
        print("\nExisting cookies found in keyring.")
        choice = input("Do you want to replace them? (y/N): ").lower()
        if choice != 'y':
            print("Keeping existing cookies.")
            return
    
    # Guide user through cookie setup
    print("\nTo set up Instagram cookies:")
    print("1. Install the Cookie-Editor browser extension")
    print("2. Log into Instagram in your browser")
    print("3. Click the Cookie-Editor extension")
    print("4. Click 'Export' -> 'Netscape HTTP Cookie File'")
    print("5. Save the content to a temporary file")
    
    cookie_file = input("\nEnter path to cookie file (or press Enter to cancel): ").strip()
    if not cookie_file:
        print("Setup cancelled.")
        return
    
    cookie_path = Path(cookie_file)
    if not cookie_path.exists():
        print(f"Error: File not found: {cookie_file}")
        return
    
    if manager.save_cookies_to_keyring(cookie_path):
        print("\n✅ Cookies successfully saved to system keyring!")
        print(f"You can now delete the temporary cookie file: {cookie_file}")
    else:
        print("\n❌ Failed to save cookies to keyring")
        sys.exit(1)

if __name__ == "__main__":
    setup_cookies()