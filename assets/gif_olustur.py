"""README animasyonunu (demo.gif) Pillow ile çizer.

Kullanım: python gif_olustur.py <cikti.gif> <onizleme_klasoru>
Her kare 2 kat büyük çizilip küçültülür (yumuşak kenarlar). Sahneler 15 kare/sn işlenir,
birbirinin aynısı kareler tek karede birleştirilir, böylece dosya küçük kalır.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S = 960, 540, 2
OW, OH = 720, 405  # GIF çıkış boyutu
FPS = 15
RENK = 96
FD = "C:/Windows/Fonts/"
BG0, BG1 = (10, 12, 17), (19, 23, 33)
PANEL, BORDER = (22, 26, 34), (46, 52, 66)
TEXT, MID, DIM = (236, 239, 244), (150, 158, 172), (84, 91, 105)
BLUE, YEL, GREEN, RED = (92, 170, 236), (247, 199, 70), (110, 205, 135), (238, 98, 88)
REPO = "github.com/findaeth/dublaj-prompter"


def sc(v):
    return int(round(v * S))


def font(name, size):
    return ImageFont.truetype(FD + name, sc(size))


F = {"title": font("segoeuib.ttf", 30), "sub": font("segoeui.ttf", 16), "h": font("segoeuib.ttf", 15),
     "s": font("segoeui.ttf", 16), "sm": font("segoeui.ttf", 13), "m": font("segoeui.ttf", 19),
     "c": font("segoeuisl.ttf", 13.5), "n": font("segoeuib.ttf", 14), "mono": font("consola.ttf", 19),
     "big": font("segoeuib.ttf", 66), "tag": font("segoeui.ttf", 16), "lead": font("segoeui.ttf", 21),
     "leadb": font("segoeuib.ttf", 21), "monosm": font("consola.ttf", 16)}


def clamp(v):
    return max(0.0, min(1.0, v))


def ease(t):
    return 1 - (1 - clamp(t)) ** 3


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    t = clamp(t)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Cv:
    """Mantıksal (960x540) koordinatla çizen sarmalayıcı."""

    def __init__(self, im):
        self.im = im
        self.d = ImageDraw.Draw(im)

    def t(self, x, y, s, f, fill, a="lm"):
        self.d.text((sc(x), sc(y)), s, font=f, fill=fill, anchor=a)

    def rr(self, box, r, fill=None, outline=None):
        self.d.rounded_rectangle([sc(v) for v in box], sc(r), fill=fill, outline=outline, width=S if outline else 1)

    def ell(self, box, fill):
        self.d.ellipse([sc(v) for v in box], fill=fill)

    def tl(self, s, f):
        return self.d.textlength(s, font=f) / S


_BG = None


def bg():
    global _BG
    if _BG is None:
        size = (W * S, H * S)
        im = Image.composite(Image.new("RGB", size, BG1), Image.new("RGB", size, BG0),
                             Image.linear_gradient("L").resize(size))
        glow = Image.new("L", size, 0)
        gd = ImageDraw.Draw(glow)
        gd.ellipse((sc(640), sc(-260), sc(1180), sc(240)), fill=46)
        gd.ellipse((sc(-200), sc(380), sc(300), sc(700)), fill=22)
        glow = glow.filter(ImageFilter.GaussianBlur(sc(90)))
        _BG = Image.composite(Image.new("RGB", size, (60, 120, 200)), im, glow)
    return _BG.copy()


def panel(c, box, title):
    x0, y0, x1, y1 = box
    c.rr(box, 14, fill=PANEL, outline=BORDER)
    for i, col in enumerate((RED, YEL, GREEN)):
        c.ell((x0 + 14 + i * 18, y0 + 12, x0 + 24 + i * 18, y0 + 22), col)
    c.t(x0 + 74, y0 + 17, title, F["sm"], MID)
    c.d.line((sc(x0 + 1), sc(y0 + 36), sc(x1 - 1), sc(y0 + 36)), fill=BORDER, width=S)


def base(idx, title, sub, panels):
    im = bg()
    sh = Image.new("L", im.size, 0)
    sd = ImageDraw.Draw(sh)
    for b, _ in panels:
        sd.rounded_rectangle((sc(b[0]), sc(b[1] + 12), sc(b[2]), sc(b[3] + 12)), sc(14), fill=170)
    im.paste((0, 0, 0), mask=sh.filter(ImageFilter.GaussianBlur(sc(18))))
    c = Cv(im)
    c.ell((60, 48, 92, 80), BLUE)
    c.t(76, 64, str(idx + 1), F["h"], BG0, "mm")
    c.t(108, 62, title, F["title"], TEXT)
    c.t(108, 98, sub, F["sub"], MID)
    for b, tt in panels:
        panel(c, b, tt)
    return im


def footer(c, idx, p, repo=True):
    if repo:
        c.t(60, 512, REPO, F["sm"], DIM)
    for i in range(4):
        x = 768 + i * 34
        c.rr((x, 508, x + 28, 513), 2, fill=BORDER)
        w = 28 if i < idx else (28 * clamp(p) if i == idx else 0)
        if w > 1:
            c.rr((x, 508, x + w, 513), 2, fill=BLUE)


def final(im):
    return im.resize((OW, OH), Image.LANCZOS)


# ---------- Sahne 1: terminal ----------
def scene1():
    dur = 6.0
    b = base(0, "Linki ver, transkript çıksın", "Tek komut: ses indirilir, konuşma yazıya dökülür",
             [((60, 140, 900, 480), "terminal")])
    seg = [("$ ", GREEN), ("python hazirla.py ", TEXT), ('"<youtube linki>"', YEL)]
    full = "".join(s for s, _ in seg)
    steps = [("Ses indiriliyor (yt-dlp)", 1.9, 2.7, 252), ("Whisper: transkript ve kelime zamanları", 2.7, 3.9, 300),
             ("ffmpeg: konuşma sessizlikleri bulunuyor", 3.9, 4.6, 348)]
    for k in range(int(dur * FPS)):
        t = k / FPS
        c = Cv(b.copy())
        n = int(len(full) * clamp((t - 0.35) / 1.4))
        x, rem = 92, n
        for s, col in seg:
            part = s[:rem]
            rem -= len(part)
            if part:
                c.t(x, 196, part, F["mono"], col)
                x += c.tl(part, F["mono"])
        if t < 2.0 and (n < len(full) or (k // 5) % 2 == 0):
            c.rr((x + 2, 184, x + 12, 208), 1, fill=TEXT)
        for label, s, e, y in steps:
            if t < s:
                continue
            a = ease((t - s) / 0.25)
            yy = y + (1 - a) * 8
            done = t >= e
            if done:
                c.ell((92, yy - 9, 110, yy + 9), mix(PANEL, GREEN, a))
                c.d.line([(sc(97), sc(yy)), (sc(100), sc(yy + 3.5)), (sc(106), sc(yy - 3.5))], fill=PANEL,
                         width=sc(2), joint="curve")
            else:
                c.d.arc([sc(92), sc(yy - 9), sc(110), sc(yy + 9)], (t * 540) % 360, (t * 540) % 360 + 270,
                        fill=mix(PANEL, YEL, a), width=sc(2.5))
            c.t(126, yy, label, F["mono"], mix(PANEL, TEXT if done else MID, a))
            if label.startswith("Whisper"):
                pr = clamp((t - s) / (e - s))
                c.rr((600, yy - 4, 840, yy + 4), 4, fill=BORDER)
                if pr > 0.02:
                    c.rr((600, yy - 4, 600 + 240 * pr, yy + 4), 4, fill=GREEN if done else BLUE)
        if t >= 4.8:
            a = ease((t - 4.8) / 0.3)
            yy = 416 + (1 - a) * 8
            c.ell((92, yy - 9, 110, yy + 9), mix(PANEL, GREEN, a))
            c.d.line([(sc(97), sc(yy)), (sc(100), sc(yy + 3.5)), (sc(106), sc(yy - 3.5))], fill=PANEL,
                     width=sc(2), joint="curve")
            c.t(126, yy, "Hazır: en.txt ve ritim.json", F["mono"], mix(PANEL, GREEN, a))
        footer(c, 0, t / dur)
        yield final(c.im)


# ---------- Sahne 2: çeviri ----------
EN = [("0:00", "A PLC is a rugged industrial computer"), ("0:07", "It reads inputs from sensors"),
      ("0:15", "Let's look at the scan cycle")]
TR = [("n", "[0:00 - GİRİŞ]"), ("c", 'EN  "A PLC is a rugged" ... "factory control"'),
      ("t", "PLC (Pi-El-Si), fabrikalarda kullanılan,"), ("t", "zorlu koşullara dayanıklı"),
      ("t", "bir endüstriyel bilgisayardır."), ("n", "[0:07]"),
      ("c", 'EN  "It reads inputs" ... "on or off"'), ("t", "Sensörlerden gelen girişleri okur,")]
KIND = {"n": (F["n"], YEL), "c": (F["c"], BLUE), "t": (F["s"], TEXT)}


def scene2():
    dur = 6.4
    b = base(1, "Claude Code Türkçeye çevirir", "Anlam sırası korunur, metin konuşma Türkçesiyle yazılır",
             [((60, 140, 450, 480), "en.txt"), ((510, 140, 900, 480), "prompter.txt")])
    for k in range(int(dur * FPS)):
        t = k / FPS
        c = Cv(b.copy())
        c.t(480, 312, "→", F["title"], mix(DIM, BLUE, (t - 1.5) / 0.4), "mm")
        for i, (ts, s) in enumerate(EN):
            a = ease((t - (0.4 + i * 0.6)) / 0.35)
            if a <= 0:
                continue
            y = 196 + i * 100 + (1 - a) * 10
            c.t(84, y, f"[{ts}]", F["sm"], mix(PANEL, BLUE, a))
            c.t(84, y + 26, s, F["s"], mix(PANEL, TEXT, a))
        for i, (kind, text) in enumerate(TR):
            a = ease((t - (1.8 + i * 0.32)) / 0.3)
            if a <= 0:
                continue
            f, col = KIND[kind]
            c.t(534, 196 + i * 36 + (1 - a) * 10, text, f, mix(PANEL, col, a))
        footer(c, 1, t / dur)
        yield final(c.im)


# ---------- Sahne 3: prompter ----------
ELEMS = [(0, "n", "[0:00 - GİRİŞ]"), (0, "c", 'EN  "A PLC is a rugged" ... "factory control"'),
         (0, "t", "PLC (Pi-El-Si), fabrikalarda kullanılan,"), (2.3, "t", "zorlu koşullara dayanıklı"),
         (4.6, "t", "bir endüstriyel bilgisayardır."), (7, "n", "[0:07]"),
         (7, "c", 'EN  "It reads inputs" ... "on or off"'), (7, "t", "Sensörlerden gelen girişleri okur,"),
         (9.3, "t", "programa göre hesaplar,"), (11.6, "t", "sonra çıkışları sürer."),
         (15, "n", "[0:15 - SAHNE GEÇİŞİ - 2 SANİYE BEKLE]"),
         (15, "c", 'EN  "Let\'s look at the scan cycle" ... "then repeats"'),
         (15, "t", "Şimdi tarama döngüsüne bakalım:"), (17.5, "t", "önce girişler okunur, program çalışır,"),
         (19.2, "t", "sonra çıkışlar güncellenir.")]
HEIGHT = {"n": 30, "c": 26, "t": 38}
YS = []
_y = 0
for _, _k, _ in ELEMS:
    YS.append(_y + HEIGHT[_k] / 2)
    _y += HEIGHT[_k]
PAUSE = (3.3, 4.3)  # konuşmacının nefes aldığı an (video saniyesi)
VW, VH = 408, 230
PW, PH, CY = 356, 206, 100


def konusma(t):
    if t <= PAUSE[0]:
        return t
    return PAUSE[0] if t <= PAUSE[1] else t - (PAUSE[1] - PAUSE[0])


def video_frame(vt, paused):
    v = Image.new("RGB", (sc(VW), sc(VH)), (12, 20, 34))
    d = ImageDraw.Draw(v)
    for y in range(0, VH // 2 + 1):
        c = int(24 + y * 0.55)
        d.rectangle((0, sc(y), sc(VW), sc(y + 1)), fill=(c // 2 + 6, c + 8, int(c * 1.55) + 14))
    d.polygon([(0, sc(VH)), (sc(VW), sc(VH)), (sc(250), sc(VH // 2)), (sc(158), sc(VH // 2))], fill=(32, 36, 45))
    ph = (vt * 0.9) % 1.0
    for i in range(7):
        p = ((i + ph) % 7) / 7.0
        yy = VH // 2 + p * p * (VH // 2)
        h, w = 3 + p * 20, 1 + p * 5
        d.rectangle((sc(204 - w), sc(yy), sc(204 + w), sc(yy + h)), fill=YEL)
    cx, cy = sc(204), sc(112)
    d.ellipse((cx - sc(26), cy - sc(26), cx + sc(26), cy + sc(26)), fill=(10, 14, 22))
    if paused:
        for dx in (-7, 3):
            d.rectangle((cx + sc(dx), cy - sc(10), cx + sc(dx + 5), cy + sc(10)), fill=(255, 255, 255))
    else:
        d.polygon([(cx - sc(7), cy - sc(11)), (cx - sc(7), cy + sc(11)), (cx + sc(12), cy)], fill=(255, 255, 255))
    m = Image.new("L", v.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, v.size[0] - 1, v.size[1] - 1), sc(10), fill=255)
    return v, m


def karaoke(pane, pd, x, y, text, ts, te, vt, barbg):
    ps = (konusma(vt) - konusma(ts)) / ((konusma(te) - konusma(ts)) or 1)
    words = text.split(" ")
    top = sum(len(w) + 1 for w in words)
    sp = pd.textlength(" ", font=F["m"]) / S
    cum = 0
    for w in words:
        a, b = cum / top, (cum + len(w) + 1) / top
        f = clamp((ps - a) / (b - a))
        wd = pd.textlength(w, font=F["m"]) / S
        pd.text((sc(x), sc(y)), w, font=F["m"], fill=(108, 117, 134), anchor="lm")
        if f > 0:
            tmp = Image.new("RGB", (sc(wd) + 4, sc(30)), barbg)
            ImageDraw.Draw(tmp).text((0, sc(15)), w, font=F["m"], fill=TEXT, anchor="lm")
            pane.paste(tmp.crop((0, 0, max(1, int(sc(wd) * f) + 1), sc(30))), (sc(x), sc(y) - sc(15)))
        if w == "PLC" and f > 0.05:
            pd.text((sc(x), sc(y + 19)), "EN: PLC", font=F["c"], fill=BLUE, anchor="lm")
        x += wd + sp
        cum += len(w) + 1


def scene3():
    dur = 8.8
    b = base(2, "Prompter videoyla birlikte akar", "Metin videonun saniyesine göre kayar, kelimeler konuşmayla dolar",
             [((60, 140, 500, 470), "Video sekmesi"), ((520, 140, 900, 470), "Prompter sekmesi")])
    barbg = mix(PANEL, BLUE, 0.10)
    mask = Image.new("L", (sc(PW), sc(PH)), 255)
    grad = Image.linear_gradient("L").resize((sc(PW), sc(38)))
    mask.paste(grad, (0, 0))
    mask.paste(grad.transpose(Image.FLIP_TOP_BOTTOM), (0, sc(PH) - sc(38)))
    solid = Image.new("RGB", mask.size, PANEL)
    off = None
    for k in range(int(dur * FPS)):
        t = k / FPS
        vt = 1.9 * t
        if t >= 3.8:
            vt = min(19.8, vt + 5 * ease((t - 3.8) / 0.3))
        paused = PAUSE[0] <= vt < PAUSE[1]
        c = Cv(b.copy())
        v, vm = video_frame(vt, paused)
        c.im.paste(v, (sc(76), sc(172)), vm)
        c.rr((76, 424, 484, 430), 3, fill=BORDER)
        c.rr((76, 424, 76 + VW * vt / 20, 430), 3, fill=RED)
        c.t(76, 448, f"{int(vt) // 60}:{int(vt) % 60:02d} / 0:20", F["sm"], MID)
        if paused:
            c.t(484, 448, "Konuşmacı duraklıyor", F["sm"], YEL, "rm")
        act = max(i for i, e in enumerate(ELEMS) if e[1] == "t" and e[0] <= vt)
        target = CY - YS[act]
        off = target if off is None else off + (target - off) * 0.14
        pane = Image.new("RGB", (sc(PW), sc(PH)), PANEL)
        pd = ImageDraw.Draw(pane)
        pd.rounded_rectangle((0, sc(CY - 19), sc(PW), sc(CY + 19)), sc(8), fill=barbg)
        pd.rounded_rectangle((0, sc(CY - 12), sc(3), sc(CY + 12)), sc(1), fill=BLUE)
        for i, (te0, kind, text) in enumerate(ELEMS):
            y = YS[i] + off
            if y < -30 or y > PH + 30:
                continue
            if kind == "t" and i == act:
                te = next((e[0] for e in ELEMS[i + 1:] if e[1] == "t"), 20)
                karaoke(pane, pd, 16, y, text, te0, te, vt, barbg)
            elif kind == "t":
                pd.text((sc(16), sc(y)), text, font=F["m"], fill=DIM if i < act else MID, anchor="lm")
            elif kind == "n":
                pd.text((sc(16), sc(y)), text, font=F["n"], fill=YEL if i > act else (96, 84, 42), anchor="lm")
            else:
                pd.text((sc(16), sc(y)), text, font=F["c"], fill=BLUE if i > act else (46, 82, 112), anchor="lm")
        c.im.paste(Image.composite(pane, solid, mask), (sc(532), sc(172)))
        x = 554
        for label, w in (("-10", 44), ("-5", 44), ("Oynat/Durdur", 104), ("+5", 44), ("+10", 44)):
            hot = label == "+5" and 3.55 <= t < 3.95
            c.rr((x, 392, x + w, 424), 8, fill=BLUE if hot else (34, 39, 49), outline=BORDER)
            c.t(x + w / 2, 408, label, F["sm"], BG0 if hot else TEXT, "mm")
            x += w + 8
        c.t(710, 448, "Karaoke açık · ritim: v3, çapa 2/9", F["sm"], MID, "mm")
        footer(c, 2, t / dur)
        yield final(c.im)


# ---------- Sahne 4: kapanış ----------
def scene4():
    dur = 7.5
    b = bg()
    tags = ["Whisper", "Karaoke", "Konuşma ritmi", "Claude Code", "Yerel"]
    last = None
    for k in range(int(dur * FPS)):
        t = k / FPS
        if t > 3.6 and last is not None:
            yield last
            continue
        c = Cv(b.copy())
        a = ease(t / 0.7)
        c.t(W / 2, 178 + (1 - a) * 22, "Dublaj Prompter", F["big"], mix(BG0, TEXT, a), "mm")
        a = ease((t - 0.35) / 0.7)
        c.t(W / 2, 244 + (1 - a) * 14, "İngilizce videolara Türkçe seslendirme için,", F["lead"], mix(BG0, MID, a), "mm")
        c.t(W / 2, 276 + (1 - a) * 14, "videoyla saniye saniye akan yerel prompter", F["lead"], mix(BG0, MID, a), "mm")
        ws = [c.tl(s, F["tag"]) + 36 for s in tags]
        x = (W - sum(ws) - 12 * (len(ws) - 1)) / 2
        for i, (s, w) in enumerate(zip(tags, ws)):
            a = ease((t - (0.9 + i * 0.14)) / 0.3)
            yy = 338 + (1 - a) * 10
            c.rr((x, yy - 17, x + w, yy + 17), 17, outline=mix(BG0, BLUE, a), fill=mix(BG0, PANEL, a))
            c.t(x + w / 2, yy, s, F["tag"], mix(BG0, BLUE, a), "mm")
            x += w + 12
        a = ease((t - 2.0) / 0.5)
        w1, w2 = c.tl("Geliştirici: ", F["lead"]), c.tl("findaeth", F["leadb"])
        x = (W - w1 - w2) / 2
        yy = 410 + (1 - a) * 10
        c.t(x, yy, "Geliştirici: ", F["lead"], mix(BG0, MID, a))
        c.t(x + w1, yy, "findaeth", F["leadb"], mix(BG0, BLUE, a))
        a = ease((t - 2.4) / 0.5)
        c.t(W / 2, 448 + (1 - a) * 10, REPO, F["monosm"], mix(BG0, DIM, a), "mm")
        footer(c, 3, 1, repo=False)
        last = final(c.im)
        yield last


def timeline():
    prev = None
    for sahne in (scene1, scene2, scene3, scene4):
        ilk = True
        for im in sahne():
            if ilk and prev is not None:
                for i in range(1, 4):
                    yield Image.blend(prev, im, smooth(i / 4))
            ilk = False
            yield im
            prev = im


def main(hedef, onizleme):
    ornek, n = [], 0
    for i, im in enumerate(timeline()):
        n += 1
        if i % 9 == 0:
            ornek.append(im.resize((OW // 2, OH // 2)))
    mozaik = Image.new("RGB", (OW // 2, (OH // 2) * len(ornek)))
    for i, o in enumerate(ornek):
        mozaik.paste(o, (0, i * (OH // 2)))
    pal = mozaik.quantize(colors=RENK, method=Image.Quantize.MEDIANCUT)
    del mozaik, ornek
    os.makedirs(os.path.dirname(os.path.abspath(hedef)), exist_ok=True)
    os.makedirs(onizleme, exist_ok=True)
    kareler, sureler, son = [], [], None
    oniz = {int(n * f): ad for ad, f in (("a", 0.1), ("b", 0.2), ("c", 0.33), ("d", 0.42), ("e", 0.55), ("f", 0.7), ("g", 0.99))}
    for i, im in enumerate(timeline()):
        if i in oniz:
            im.save(os.path.join(onizleme, f"onizleme_{oniz[i]}.png"))
        q = im.quantize(palette=pal, dither=Image.Dither.NONE)
        by = q.tobytes()
        if by == son:
            sureler[-1] += 1000 // FPS
        else:
            kareler.append(q)
            sureler.append(1000 // FPS)
            son = by
    sureler[-1] += 2500
    kareler[0].save(hedef, save_all=True, append_images=kareler[1:], duration=sureler, loop=0, optimize=False, disposal=1)
    print(n, "kare ->", len(kareler), "benzersiz,", round(os.path.getsize(hedef) / 1024), "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
