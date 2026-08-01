#!/usr/bin/env python3
"""
Simple on-device pipeline:
- Convert input to WAV, mono, 22050 Hz
- Extract last SEED_SECONDS of audio as seed
- Loop + crossfade the seed to make an extended vocal snippet
- Generate a short continuation text (simple Markov-like or template)
- Synthesize continuation with gTTS (requires internet)
- Mix seed-loop + TTS into a final out file
"""

import os
import subprocess
import uuid
from gtts import gTTS
import shlex

SEED_SECONDS = 3
EXTENDED_SECONDS = 10

def run(cmd):
    print("[run]", cmd)
    ret = subprocess.run(cmd, shell=True)
    if ret.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def safe_basename(path):
    return os.path.basename(path)

def convert_to_wav(in_path, out_wav):
    cmd = f'ffmpeg -y -i "{in_path}" -ar 22050 -ac 1 -vn "{out_wav}"'
    run(cmd)

def extract_seed(wav_in, seed_out, seconds=SEED_SECONDS):
    # -sseof -N extracts last N seconds
    cmd = f'ffmpeg -y -sseof -{seconds} -i "{wav_in}" -ar 22050 -ac 1 -vn "{seed_out}"'
    run(cmd)

def make_loop(seed_wav, loop_out, duration=EXTENDED_SECONDS):
    # loop by concatenating same file several times with small crossfade
    # simple approach: stream_loop and then trim; add tiny fade in/out
    cmd = f'ffmpeg -y -stream_loop 10 -i "{seed_wav}" -af "afade=t=in:ss=0:d=0.05,afade=t=out:st={duration-0.05}:d=0.05" -t {duration} "{loop_out}"'
    run(cmd)

def pitch_shift(in_wav, out_wav, semitone_shift=0.8):
    # approximate pitch shift by changing rate then resampling
    factor = 2 ** (semitone_shift / 12.0)
    cmd = f'ffmpeg -y -i "{in_wav}" -af "asetrate=22050*{factor},aresample=22050" "{out_wav}"'
    run(cmd)

def simple_text_continuation(seed_text):
    """
    Very simple continuation:
    - If seed_text provided, repeat last line and append a 6-12 word continuation generated from its words.
    - Otherwise, use a generic template.
    """
    if not seed_text:
        return "And it keeps going, the melody continues and the chorus comes back."
    # last few words
    words = seed_text.strip().split()
    if not words:
        return "And it keeps going, the melody continues and the chorus comes back."
    tail = words[-6:]
    # generate small continuation by rotating words and adding filler
    cont = " ".join(tail) + " ... and it goes on, singing about the same feeling and more."
    return cont

def synthesize_tts(text, out_mp3):
    # gTTS writes mp3
    tts = gTTS(text=text, lang="en")
    tts.save(out_mp3)

def mix_audio(a_path, b_path, out_path):
    # a_path and b_path -> amix
    cmd = f'ffmpeg -y -i "{a_path}" -i "{b_path}" -filter_complex "[0:a]volume=0.9[a];[1:a]volume=0.9[b];[a][b]amix=inputs=2:duration=shortest,volume=2" -ar 22050 "{out_path}"'
    run(cmd)

def optionally_transcribe_seed(seed_wav):
    """
    If whisper.cpp or another small offline binary is present at ./whisper_local,
    call it and return the transcription. Otherwise return empty string.
    """
    whisper_bin = "./whisper_local"  # placeholder: user can build whisper.cpp and name binary whisper_local
    if os.path.exists(whisper_bin) and os.access(whisper_bin, os.X_OK):
        # example: whisper_local -m tiny.en.ggml -f seed.wav --output-txt
        cmd = f'{whisper_bin} -m tiny.en.ggml -f "{seed_wav}"'
        try:
            run(cmd)
            # assume it writes seed_wav.txt
            txt_path = seed_wav + ".txt"
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as fh:
                    return fh.read().strip()
        except Exception:
            return ""
    return ""

def process_upload(in_path, out_dir="out"):
    try:
        uid = uuid.uuid4().hex[:8]
        base = os.path.splitext(safe_basename(in_path))[0]
        wav = os.path.join("/tmp", f"{base}_{uid}.wav")
        seed = os.path.join("/tmp", f"{base}_{uid}_seed.wav")
        seed_loop = os.path.join("/tmp", f"{base}_{uid}_seed_loop.wav")
        pitched = os.path.join("/tmp", f"{base}_{uid}_pitched.wav")
        tts_mp3 = os.path.join("/tmp", f"{base}_{uid}_tts.mp3")
        final_out = os.path.join(out_dir, f"{base}_{uid}_out.mp3")

        # convert to wav
        convert_to_wav(in_path, wav)
        # extract seed
        extract_seed(wav, seed, seconds=SEED_SECONDS)
        # try lightweight transcription (optional)
        seed_text = optionally_transcribe_seed(seed)
        # loop seed
        make_loop(seed, seed_loop, duration=EXTENDED_SECONDS)
        # pitch shift for variation
        pitch_shift(seed_loop, pitched, semitone_shift=0.6)
        # generate continuation text
        cont = simple_text_continuation(seed_text)
        # synthesize TTS
        synthesize_tts(cont, tts_mp3)
        # mix pitched seed + tts
        mix_audio(pitched, tts_mp3, final_out)
        return final_out
    except Exception as e:
        print("Processing error:", e)
        return None
