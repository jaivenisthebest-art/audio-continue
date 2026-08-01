#!/data/data/com.termux/files/usr/bin/bash
# Start the Flask server (Termux)
source venv/bin/activate
export FLASK_APP=server.py
export FLASK_ENV=production
echo "[*] Starting server on http://127.0.0.1:8000"
python server.py
