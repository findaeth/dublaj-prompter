"""YouTube linkinden zaman damgalı transkript çıkarır.

Kullanım: python hazirla.py <youtube-linki> [model]
Çıktı:    veri/<video-id>/en.json, en.txt  (ve ses.wav ara dosyası)
"""
import json
import os
import re
import shutil
import subprocess
import sys

WINGET_LINKS = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links")
if not shutil.which("ffmpeg") and os.path.isdir(WINGET_LINKS):
    os.environ["PATH"] += os.pathsep + WINGET_LINKS


def video_id(link):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", link)
    if not m:
        sys.exit("Video ID bulunamadı: " + link)
    return m.group(1)


def stamp(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    link = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "small"
    vid = video_id(link)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri", vid)
    os.makedirs(out, exist_ok=True)

    ham = os.path.join(out, "ham.%(ext)s")
    subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--no-playlist", "--js-runtimes", "node",
         "-f", "bestaudio", "-o", ham, "--no-progress",
         "https://www.youtube.com/watch?v=" + vid],
        check=True,
    )
    ham_dosya = next(f for f in os.listdir(out) if f.startswith("ham."))
    wav = os.path.join(out, "ses.wav")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", os.path.join(out, ham_dosya),
         "-vn", "-ac", "1", "-ar", "16000", wav],
        check=True,
    )

    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, info = model.transcribe(wav, vad_filter=True)
    veri = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
            for s in segs]

    with open(os.path.join(out, "en.json"), "w", encoding="utf-8") as f:
        json.dump({"id": vid, "dil": info.language, "segmentler": veri}, f,
                  ensure_ascii=False, indent=1)
    with open(os.path.join(out, "en.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"[{stamp(s['start'])}] {s['text']}" for s in veri))

    os.remove(os.path.join(out, ham_dosya))
    os.remove(wav)
    print(f"{vid}: dil={info.language}, {len(veri)} segment -> {out}")


if __name__ == "__main__":
    main()
