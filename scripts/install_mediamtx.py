#!/usr/bin/env python3

import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from urllib.request import urlretrieve

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MEDIAMTX_DIR = PROJECT_ROOT / "src" / "streamweaver" / "thirdparty" / "mediamtx"
MEDIAMTX_BINARY = MEDIAMTX_DIR / "mediamtx"


def is_mediamtx_installed():
    """Check if mediamtx binary already exists locally."""
    return MEDIAMTX_BINARY.exists()


def download_mediamtx(version="latest"):
    """Download mediamtx binary based on system architecture."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux" and machine in ["x86_64", "amd64"]:
        platform_tag = "linux_amd64"
    elif system == "darwin" and machine in ["x86_64", "amd64"]:
        platform_tag = "darwin_amd64"
    else:
        print(f"Unsupported system/architecture: {system} {machine}")
        sys.exit(1)

    if version == "latest":
        version = "v1.12.0"  # Pin a stable known version

    filename = f"mediamtx_{version}_{platform_tag}.tar.gz"
    url = (
        f"https://github.com/bluenviron/mediamtx/releases/download/{version}/{filename}"
    )

    print(f"Downloading {url}...")
    tmp_dir = tempfile.mkdtemp()
    archive_path = os.path.join(tmp_dir, filename)
    urlretrieve(url, archive_path)

    return archive_path, tmp_dir


def extract_and_install(archive_path, tmp_dir):
    """Extract mediamtx binary and place it in thirdparty folder."""
    print("Extracting archive...")
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=tmp_dir)

    extracted_binary = os.path.join(tmp_dir, "mediamtx")
    if not os.path.exists(extracted_binary):
        print("mediamtx binary not found after extraction.")
        sys.exit(1)

    MEDIAMTX_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Installing mediamtx to {MEDIAMTX_DIR} ...")
    shutil.move(extracted_binary, MEDIAMTX_BINARY)
    os.chmod(MEDIAMTX_BINARY, 0o755)


def verify_installation():
    """Verify the local mediamtx binary works."""
    try:
        result = subprocess.run(
            [str(MEDIAMTX_BINARY), "-h"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ mediamtx installed successfully inside thirdparty directory!")
        else:
            print("Something went wrong running mediamtx.")
            sys.exit(1)
    except FileNotFoundError:
        print("mediamtx binary not found.")
        sys.exit(1)


def main():
    if is_mediamtx_installed():
        print(f"✅ mediamtx already installed at {MEDIAMTX_BINARY}")
        sys.exit(0)

    archive_path, tmp_dir = download_mediamtx()
    extract_and_install(archive_path, tmp_dir)
    verify_installation()


if __name__ == "__main__":
    main()
