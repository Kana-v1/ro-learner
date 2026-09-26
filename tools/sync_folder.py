"""
Where the app's sync folder is on this PC: the folder the phone links (iCloud
Drive, synced to Windows by iCloud for Windows), holding lessons/, results/
and notes/.

Taken from $VORBESTE_SYNC, else from the first line of sync_folder.txt in the
project root (gitignored: a personal path, kept out of the public repo), e.g.

    /mnt/c/Users/you/iCloudDrive/Vorbește

None when neither is set; the scripts then keep everything local.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # the project root
CONFIG = ROOT / "sync_folder.txt"


def sync_folder():
    value = os.environ.get("VORBESTE_SYNC", "").strip()
    if not value and CONFIG.exists():
        lines = CONFIG.read_text(encoding="utf-8").split("\n")
        value = lines[0].strip()
    if not value:
        return None
    folder = Path(value)
    if not folder.is_dir():
        print(f"sync folder {folder} is not there (is iCloud for Windows running?); keeping files local")
        return None
    return folder
