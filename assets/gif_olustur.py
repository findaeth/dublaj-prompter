import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 405
BG = (15, 17, 21); PANEL = (24, 27, 33); BORDER = (48, 52, 62)
TEXT = (235, 237, 240); DIM = (78, 83, 93); MID = (140, 146, 158)
BLUE = (90, 169, 230); YEL = (245, 197, 66); GREEN = (110, 200, 130); RED = (235, 95, 86)
FD = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


f_t = font("segoeuib.ttf", 20); f_h = font("segoeuib.ttf", 13); f_s = font("segoeui.ttf", 13)
f_m = font("segoeui.ttf", 16); f_mb = font("segoeuib.ttf", 16); f_c = font("segoeuisl.ttf", 12)
f_n = font("segoeuib.ttf", 12); f_mono = font("consola.ttf", 15); f_big = font("segoeuib.ttf", 44)
f_sub = font("segoeui.ttf", 18)


def base(step, title):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.ellipse((30, 22, 54, 46), fill=BLUE)
    d.text((42, 34), str(step), font=f_h, fill=BG, anchor="mm")
    d.text((66, 34), title, font=f_t, fill=TEXT, anchor="lm")
    for i in range(4):
        x = W / 2 - 36 + i * 24
        d.ellipse((x, H - 24, x + 10, H - 14), fill=BLUE if i == step - 1 else BORDER)
    return im, d


def panel(d, box, title):
    d.rounded_rectangle(box, 10, fill=PANEL, outline=BORDER)
    x0, y0 = box[0], box[1]
    for i, c in enumerate((RED, YEL, GREEN)):
        d.ellipse((x0 + 12 + i * 16, y0 + 10, x0 + 22 + i * 16, y0 + 20), fill=c)
    d.text((x0 + 66, y0 + 15), title, font=f_s, fill=MID, anchor="lm")


def scene_a(n=36):
    out = []
    cmd = '$ python hazirla.py "<youtube linki>"'
    for k in range(n):
        im, d = base(1, "Linki ver, transkript çıksın")
        panel(d, (30, 70, 690, 330), "terminal")
        typed = cmd[:min(len(cmd), int(k * len(cmd) / 13))]
        d.text((52, 114), typed, font=f_mono, fill=TEXT, anchor="lm")
        if k < 14 and k % 4 < 2:
            x = 52 + d.textlength(typed, font=f_mono)
            d.rectangle((x + 2, 104, x + 10, 124), fill=TEXT)
        for label, s, e, y in (("Ses indiriliyor (yt-dlp)", 15, 20, 164),
                               ("Whisper: transkript ve kelime zamanları", 20, 28, 198),
                               ("ffmpeg: konuşma sessizlikleri bulunuyor", 28, 32, 232)):
            if k >= s:
                done = k >= e
                d.ellipse((52, y - 6, 64, y + 6), fill=GREEN if done else YEL)
                d.text((76, y), label, font=f_mono, fill=TEXT if done else MID, anchor="lm")
        if 20 <= k < 28:
            d.rounded_rectangle((76, 222, 476, 230), 4, fill=BORDER)
            d.rounded_rectangle((76, 222, 76 + int(400 * (k - 20) / 8), 230), 4, fill=BLUE)
        if k >= 32:
            d.text((76, 270), "Hazır: en.txt ve ritim.json", font=f_mono, fill=GREEN, anchor="lm")
        out.append(im)
    return out


EN = [("0:00", "A PLC is a rugged industrial computer"),
      ("0:07", "It reads inputs from sensors"),
      ("0:15", "Let's look at the scan cycle")]
TR = [("n", "[0:00 - GİRİŞ]"), ("c", 'EN  "A PLC is a rugged" ... "factory control"'),
      ("t", "PLC (Pi-El-Si), fabrikalarda kullanılan,"), ("t", "zorlu koşullara dayanıklı"),
      ("t", "bir endüstriyel bilgisayardır."), ("n", "[0:07]"),
      ("c", 'EN  "It reads inputs" ... "on or off"'), ("t", "Sensörlerden gelen girişleri okur,")]


def draw_item(d, kind, text, x, y, color=None):
    if kind == "n":
        d.text((x, y), text, font=f_n, fill=color or YEL, anchor="lm")
    elif kind == "c":
        d.text((x, y), text, font=f_c, fill=color or BLUE, anchor="lm")
    else:
        d.text((x, y), text, font=f_s, fill=color or TEXT, anchor="lm")


def scene_b(n=34):
    out = []
    for k in range(n):
        im, d = base(2, "Claude Code Türkçeye çevirir")
        panel(d, (30, 70, 340, 330), "en.txt")
        panel(d, (380, 70, 690, 330), "prompter.txt")
        d.text((360, 200), "→", font=f_t, fill=MID, anchor="mm")
        for i, (t, s) in enumerate(EN):
            if k >= 2 + i * 3:
                y = 124 + i * 56
                d.text((48, y), f"[{t}]", font=f_s, fill=BLUE, anchor="lm")
                d.text((48, y + 20), s, font=f_s, fill=TEXT, anchor="lm")
        for i, (kind, text) in enumerate(TR):
            if k >= 10 + i * 2:
                draw_item(d, kind, text, 398, 112 + i * 26)
        out.append(im)
    return out


ELEMS = [(0, "n", "[0:00 - GİRİŞ]"), (0, "c", 'EN  "A PLC is a rugged" ... "factory control"'),
         (0, "t", "PLC (Pi-El-Si), fabrikalarda kullanılan,"), (2.3, "t", "zorlu koşullara dayanıklı"),
         (4.6, "t", "bir endüstriyel bilgisayardır."), (7, "n", "[0:07]"),
         (7, "c", 'EN  "It reads inputs" ... "on or off"'), (7, "t", "Sensörlerden gelen girişleri okur,"),
         (9.3, "t", "programa göre hesaplar,"), (11.6, "t", "sonra çıkışları sürer."),
         (15, "n", "[0:15 - SAHNE GEÇİŞİ - 2 SANİYE BEKLE]"),
         (15, "c", 'EN  "Let\'s look at the scan cycle" ... "then repeats"'),
         (15, "t", "Şimdi tarama döngüsüne bakalım:"), (17.5, "t", "önce girişler okunur, program çalışır,"),
         (19.2, "t", "sonra çıkışlar güncellenir.")]
HEIGHT = {"n": 28, "c": 24, "t": 34}
YS = []
_y = 0
for _, kind, _ in ELEMS:
    YS.append(_y)
    _y += HEIGHT[kind]


def video_frame(k, vt):
    v = Image.new("RGB", (310, 164), (12, 20, 34))
    d = ImageDraw.Draw(v)
    for y in range(0, 80):
        c = int(30 + y * 0.6)
        d.line((0, y, 310, y), fill=(c // 2, c, int(c * 1.5)))
    d.polygon([(0, 164), (310, 164), (190, 80), (120, 80)], fill=(34, 38, 46))
    for i in range(6):
        p = ((i * 14 + k * 5) % 84) / 84.0
        yy = 80 + p * p * 84
        h = 3 + p * 14
        w = 1 + p * 4
        d.rectangle((155 - w, yy, 155 + w, yy + h), fill=YEL)
    d.polygon([(135, 110), (135, 130), (153, 120)], fill=(255, 255, 255))
    return v


PAUSE = (3.3, 4.3)  # konuşmacının nefes aldığı an (video saniyesi)


def konusma(t):
    if t <= PAUSE[0]:
        return t
    return PAUSE[0] if t <= PAUSE[1] else t - (PAUSE[1] - PAUSE[0])


def karaoke(pd, pane, x, y, text, ts, te, vt):
    ps = (konusma(vt) - konusma(ts)) / ((konusma(te) - konusma(ts)) or 1)
    kel = text.split(" ")
    top = sum(len(k) + 1 for k in kel)
    sp = pd.textlength(" ", font=f_m)
    cum = 0
    for k in kel:
        a, b = cum / top, (cum + len(k) + 1) / top
        f = min(1, max(0, (ps - a) / (b - a)))
        w = pd.textlength(k, font=f_m)
        pd.text((x, y), k, font=f_m, fill=(110, 116, 128), anchor="lm")
        if f > 0:
            tmp = Image.new("RGB", (int(w) + 4, 26), PANEL)
            ImageDraw.Draw(tmp).text((0, 13), k, font=f_m, fill=TEXT, anchor="lm")
            pane.paste(tmp.crop((0, 0, max(1, int(w * f) + 1), 26)), (int(x), y - 13))
        if k == "PLC" and f > 0.05:
            pd.text((x, y + 17), "EN: PLC", font=f_c, fill=BLUE, anchor="lm")
        x += w + sp
        cum += len(k) + 1


def scene_c(n=72):
    out = []
    off = 0.0
    for k in range(n):
        vt = k * 0.22 if k < 36 else min(19.8, k * 0.22 + 5)
        im, d = base(3, "Prompter videoyla birlikte akar")
        panel(d, (30, 70, 356, 300), "Video sekmesi")
        panel(d, (372, 70, 690, 300), "Prompter sekmesi")
        im.paste(video_frame(k, vt), (38, 96))
        d.rounded_rectangle((38, 268, 348, 274), 3, fill=BORDER)
        d.rounded_rectangle((38, 268, 38 + int(310 * vt / 20), 274), 3, fill=RED)
        d.text((38, 286), f"{int(vt)//60}:{int(vt)%60:02d} / 0:20", font=f_s, fill=MID, anchor="lm")
        act = max(i for i, e in enumerate(ELEMS) if e[1] == "t" and e[0] <= vt)
        off += ((92 - YS[act]) - off) * 0.3
        pane = Image.new("RGB", (302, 196), PANEL)
        pd = ImageDraw.Draw(pane)
        for i, (t, kind, text) in enumerate(ELEMS):
            y = YS[i] + off + 14
            if y < -20 or y > 210:
                continue
            if kind == "t" and i == act:
                te = next((e[0] for e in ELEMS[i + 1:] if e[1] == "t"), 20)
                karaoke(pd, pane, 6, int(y), text, ELEMS[i][0], te, vt)
            elif kind == "t":
                col = DIM if i < act else MID
                pd.text((6, y), text, font=f_m, fill=col, anchor="lm")
            elif kind == "n":
                pd.text((6, y), text, font=f_n, fill=YEL if i > act else (90, 80, 40), anchor="lm")
            else:
                pd.text((6, y), text, font=f_c, fill=BLUE if i > act else (45, 80, 110), anchor="lm")
        im.paste(pane, (380, 96))
        d.line((380, 96 + 92, 688, 96 + 92), fill=BORDER)
        d = ImageDraw.Draw(im)
        pressed = 36 <= k < 40
        x = 388
        for label, w in (("-10", 40), ("-5", 40), ("Oynat/Durdur", 112), ("+5", 40), ("+10", 40)):
            hot = pressed and label == "+5"
            d.rounded_rectangle((x, 308, x + w, 334), 6, fill=BLUE if hot else (36, 40, 48), outline=BORDER)
            d.text((x + w / 2, 321), label, font=f_s, fill=BG if hot else TEXT, anchor="mm")
            x += w + 8
        d.text((531, 352), "Karaoke açık · ritim: v3, çapa 2/9", font=f_s, fill=MID, anchor="mm")
        if PAUSE[0] <= vt < PAUSE[1]:
            d.text((348, 286), "Konuşmacı duraklıyor", font=f_s, fill=YEL, anchor="rm")
        out.append(im)
    return out


def scene_d(n=28):
    out = []
    bg = Image.new("RGB", (W, H), BG)
    for k in range(n):
        card = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(card)
        d.text((W / 2, 150), "Dublaj Prompter", font=f_big, fill=TEXT, anchor="mm")
        d.text((W / 2, 205), "İngilizce videolara Türkçe seslendirme için,", font=f_sub, fill=MID, anchor="mm")
        d.text((W / 2, 232), "videoyla saniye saniye akan yerel prompter", font=f_sub, fill=MID, anchor="mm")
        x = 85
        for tag, w in (("Whisper", 90), ("Karaoke", 90), ("Konuşma ritmi", 130), ("Claude Code", 120), ("Yerel", 80)):
            d.rounded_rectangle((x, 290, x + w, 318), 14, outline=BLUE, fill=PANEL)
            d.text((x + w / 2, 304), tag, font=f_s, fill=BLUE, anchor="mm")
            x += w + 10
        d.ellipse((W / 2 - 36 + 3 * 24, H - 24, W / 2 - 36 + 3 * 24 + 10, H - 14), fill=BLUE)
        a = min(1.0, k / 8)
        out.append(Image.blend(bg, card, a))
    return out


def main(hedef, onizleme):
    sahneler = [scene_a(), scene_b(), scene_c(), scene_d()]
    frames = [f for s in sahneler for f in s]
    sure = [100] * len(frames)
    for s, ek in zip(sahneler, (700, 900, 900, 2200)):
        sure[sum(len(x) for x in sahneler[:sahneler.index(s)]) + len(s) - 1] = ek
    ornek = Image.new("RGB", (W, H * 4))
    for i, s in enumerate(sahneler):
        ornek.paste(s[len(s) // 2 if i != 2 else 30], (0, H * i))
    pal = ornek.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    q[0].save(hedef, save_all=True, append_images=q[1:], duration=sure, loop=0, optimize=False, disposal=1)
    for ad, idx in (("a", 30), ("b", 60), ("c0", 73), ("c1", 85), ("c2", 120), ("d", len(frames) - 1)):
        frames[idx].save(os.path.join(onizleme, f"onizleme_{ad}.png"))
    print(len(frames), "kare,", round(os.path.getsize(hedef) / 1024), "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
