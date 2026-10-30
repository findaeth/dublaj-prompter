"""YouTube linkinden zaman damgalı transkript çıkarır.

Kullanım: python hazirla.py <youtube-linki> [model]
Çıktı:    veri/<video-id>/en.json, en.txt, ritim.json  (ve ses.wav ara dosyası)
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


def sessizlikler(wav, esik="-32dB", sure=0.18):
    """ffmpeg silencedetect ile gerçek sessizlik aralıklarını [(başlangıç, bitiş), ...] döndürür."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise={esik}:d={sure}", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    bas = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(bas, son))


def kirp(kelimeler, sess):
    """Whisper kelime sürelerini sessizliklere göre kırpar. Sessizliğe taşan kelimenin sonu sessizliğin
    başına, sessizliğin içinde başlayan kelimenin başı sessizliğin sonuna çekilir. Sessizliğin iki yanına
    yayılan kelimeye dokunulmaz. kelimeler: [[metin, başlangıç, bitiş], ...], yerinde değiştirilir."""
    for k in kelimeler:
        for s, e in sess:
            if k[1] < s < k[2] and k[2] <= e + 0.05:
                k[2] = round(max(k[1] + 0.05, s), 2)
            elif s - 0.1 <= k[1] < e < k[2]:
                k[1] = round(min(k[2] - 0.05, e), 2)
    return kelimeler


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
    segs, info = model.transcribe(wav, vad_filter=True, word_timestamps=True)
    veri = []
    kelimeler = []  # konuşmanın ritmi: her kelimenin [metin, başlangıç, bitiş] saniyesi
    for s in segs:
        veri.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        kelimeler.extend([w.word.strip(), round(w.start, 2), round(w.end, 2)] for w in (s.words or []))

    with open(os.path.join(out, "en.json"), "w", encoding="utf-8") as f:
        json.dump({"id": vid, "dil": info.language, "segmentler": veri}, f,
                  ensure_ascii=False, indent=1)
    with open(os.path.join(out, "en.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"[{stamp(s['start'])}] {s['text']}" for s in veri))

    sess = sessizlikler(wav)
    once = [list(k) for k in kelimeler]
    kirp(kelimeler, sess)
    degisen = sum(1 for a, b in zip(once, kelimeler) if a != b)
    with open(os.path.join(out, "ritim.json"), "w", encoding="utf-8") as f:
        # kelimeler: [[başlangıç, bitiş], ...] (v2 uyumlu), metinli: [[metin, başlangıç, bitiş], ...] (v3 çapalama)
        json.dump({"id": vid, "surum": 3, "kelimeler": [[k[1], k[2]] for k in kelimeler],
                   "metinli": kelimeler}, f, ensure_ascii=False)

    os.remove(os.path.join(out, ham_dosya))
    os.remove(wav)
    print(f"{vid}: dil={info.language}, {len(veri)} segment, {len(kelimeler)} kelime, "
          f"{len(sess)} sessizlik ({degisen} kelime kırpıldı) -> {out}")


if __name__ == "__main__":
    main()
