"""
The private GitHub repository the app syncs with (its README describes the
layout): episodes go up as assets of the release "episodes", results and the
app's log come down from results/ and logs/, Claude's notes go up to notes/.

Preferred over the iCloud folder (tools/sync_folder.py): iCloud uploads and
downloads when it chooses to; this is plain HTTPS and happens now.

The repo is $VORBESTE_DATA_REPO or Kana-v1/ro-learner-data, cloned next to
this project as ../ro-learner-data. The token is $GITHUB_PERSONAL_ACCESS_TOKEN
(or $GH_TOKEN), which needs Contents read/write on that repo.
"""
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # the project root
REPO = os.environ.get("VORBESTE_DATA_REPO", "Kana-v1/ro-learner-data")
CLONE = ROOT.parent / "ro-learner-data"
GH = shutil.which("gh") or str(Path.home() / ".local/bin/gh")


def _env():
    env = dict(os.environ)
    token = env.get("GH_TOKEN") or env.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if token:
        env["GH_TOKEN"] = token
    return env


def available():
    """Configured: a token, the gh tool, and the local clone."""
    return bool(_env().get("GH_TOKEN")) and Path(GH).exists() and (CLONE / ".git").is_dir()


def _git(*args):
    return subprocess.run(["git", "-C", str(CLONE), *args], env=_env(),
                          check=True, capture_output=True, text=True)


def upload_episode(path):
    """Upload (or replace) one .rolesson as an asset of the release."""
    subprocess.run([GH, "release", "upload", "episodes", str(path), "-R", REPO, "--clobber"],
                   env=_env(), check=True, capture_output=True, text=True)
    print(f"  -> GitHub {REPO}, release 'episodes': {Path(path).name}")


def pull():
    """Bring the clone up to date; returns its results/ folder."""
    _git("pull", "-q", "--rebase")
    return CLONE / "results"


def push_note(path):
    """Commit a .roanalysis into notes/ and push it; the app picks it up."""
    notes = CLONE / "notes"
    notes.mkdir(exist_ok=True)
    shutil.copy2(path, notes / Path(path).name)
    _git("add", f"notes/{Path(path).name}")
    _git("commit", "-q", "-m", f"Note {Path(path).stem}")
    _git("push", "-q")
    print(f"  -> GitHub {REPO}: notes/{Path(path).name}")
