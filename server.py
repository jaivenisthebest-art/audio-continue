#!/usr/bin/env python3
from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
import os
from pipeline import process_upload

UPLOAD_DIR = "uploads"
OUT_DIR = "out"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="static")

INDEX_HTML = open("static/index.html", "r", encoding="utf-8").read()

@app.route("/", methods=["GET"])
def index():
    return INDEX_HTML

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return {"error": "no file uploaded"}, 400
    fname = f.filename
    safe_name = fname.replace(" ", "_")
    in_path = os.path.join(UPLOAD_DIR, safe_name)
    f.save(in_path)
    # Process (synchronous for prototype)
    out_path = process_upload(in_path, OUT_DIR)
    if out_path:
        return {"ok": True, "output": os.path.basename(out_path)}
    else:
        return {"error": "processing failed"}, 500

@app.route("/out/<path:filename>")
def out_file(filename):
    return send_from_directory(OUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
