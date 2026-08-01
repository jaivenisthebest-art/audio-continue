const uploadBtn = document.getElementById("upload");
const fileInput = document.getElementById("file");
const status = document.getElementById("status");
const result = document.getElementById("result");

uploadBtn.onclick = async () => {
  const f = fileInput.files[0];
  if (!f) { alert("Pick a file first"); return; }
  status.textContent = "Uploading...";
  const fd = new FormData();
  fd.append("file", f);
  try {
    const res = await fetch("/upload", { method: "POST", body: fd });
    const data = await res.json();
    if (data.ok) {
      status.textContent = "Processing finished. Preparing download...";
      const out = data.output;
      result.innerHTML = `<a href="/out/${out}" download>Download result</a>
                          <br/><audio controls src="/out/${out}"></audio>`;
      status.textContent = "Done.";
    } else {
      status.textContent = "Error: " + (data.error || "unknown");
    }
  } catch (e) {
    status.textContent = "Upload failed: " + e;
  }
};
