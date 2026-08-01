#!/data/data/com.termux/files/usr/bin/bash
# Termux install helper for Phone-Audio-Continue
# Run: chmod +x termux_install.sh && ./termux_install.sh

set -e

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing required packages: python, ffmpeg, git, wget, termux-api..."
pkg install -y python ffmpeg git wget termux-api

echo "[*] Granting storage access (you will be prompted)..."
termux-setup-storage || true

echo "[*] Creating Python venv..."
python -m venv venv
source venv/bin/activate

echo "[*] Upgrading pip and installing python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Done. To start the server: ./run.sh"
