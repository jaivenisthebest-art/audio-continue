# Phone-Audio-Continue (Android Termux demo)

Phone-first demo that accepts an MP3/MP4 snippet and produces a short auto-completion on-device using FFmpeg + gTTS. This is a free, phone-only prototype (no heavy model, no paid APIs required). It does not do high-quality voice cloning — it repeats and varies the snippet and uses synthesized speech for the continuation.

Important: You confirmed you have consent from the person whose voice is used. Do not use this repo to impersonate or abuse others.

Contents
- termux_install.sh  — script to install Termux packages and Python deps
- run.sh             — starts the Flask server
- server.py          — Flask backend (upload endpoint)
- pipeline.py        — audio processing pipeline
- static/index.html  — minimal web UI
- requirements.txt   — Python requirements
- NOTICE_CONSENT.md  — consent & warning text
- LICENSE            — MIT license

Quick Android (Termux) setup
1. Install Termux (from F-Droid) and open it.
2. Paste the repo files into a directory in Termux (e.g., ~/audio-continue).
   - You can `git clone` after creating a repo, or copy/paste files using Termux's editor.
3. In Termux run:
   chmod +x termux_install.sh run.sh
   ./termux_install.sh
4. Start the server:
   ./run.sh
5. On your phone browser, open: http://127.0.0.1:8000
6. Upload an MP3/MP4 and wait for processing. Download the result.

If ffmpeg is installed and working, processing is done entirely on-device. gTTS uses the free Google Translate TTS endpoint (requires internet). If you want fully offline TTS, install an offline TTS app and modify pipeline.py to save TTS differently.

How to create a GitHub repo and push (if you want it on GitHub)
1. Create a new empty repository on GitHub (via the website).
2. In Termux inside the project folder:
   git init
   git add .
   git commit -m "Initial commit - Phone-Audio-Continue demo"
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main

Notes & limitations
- This demo uses a simple text-continuation algorithm and gTTS for synthesized continuation, plus loop/pitch tricks on the seed.
- True voice cloning or singing synthesis requires large models (RVC, HiFi-GAN, MusicGen) and GPUs; those are out-of-scope for free phone-only runs.
- The code includes a placeholder hook in pipeline.py (PLACEHOLDER_VOICE_CLONE) where a future API (ElevenLabs, Resemble, or RVC) can be plugged in if you later add keys.
- Keep uploaded files private and delete after use. The demo stores files in `./uploads/` and `./out/`.

If you want, I can now:
- Provide a ready-to-run ZIP of this repo (you’ll still need to upload it somewhere), or
- Add optional cloud-API hooks (you’d need to paste your API key into a config file I’ll add), or
- A one-click script that initializes a GitHub repo and pushes (you’ll need to paste your Git remote URL),

tell me which and I’ll produce it next. If you want, I can also produce an explicit README section that someone with your GitHub access can follow verbatim to create the repo and push the files — I already included that, but I can expand it into a short checklist with copy/paste commands.

Enjoy.
