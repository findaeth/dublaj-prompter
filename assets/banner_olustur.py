"""README başlık görselini (banner.png) çizer. Kullanım: python banner_olustur.py <banner.png>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from gif_olustur import BG0, BG1, BLUE, DIM, FD, MID, PANEL, TEXT

W, H, S = 1280, 300, 2


def f(name, size):
    return ImageFont.truetype(FD + name, size * S)


def main(hedef):
    size = (W * S, H * S)
    im = Image.composite(Image.new("RGB", size, BG1), Image.new("RGB", size, BG0), Image.linear_gradient("L").resize(size))
    glow = Image.new("L", size, 0)
    ImageDraw.Draw(glow).ellipse((820 * S, -200 * S, 1400 * S, 260 * S), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(90 * S))
    im = Image.composite(Image.new("RGB", size, (60, 120, 200)), im, glow)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90 * S, 78 * S, 98 * S, 168 * S), 4 * S, fill=BLUE)
    d.text((122 * S, 100 * S), "Dublaj Prompter", font=f("segoeuib.ttf", 64), fill=TEXT, anchor="lm")
    d.text((124 * S, 156 * S), "İngilizce videolara Türkçe seslendirme için, videoyla saniye saniye akan yerel prompter",
           font=f("segoeui.ttf", 21), fill=MID, anchor="lm")
    x = 124 * S
    ft = f("segoeui.ttf", 16)
    for tag in ("Whisper", "Karaoke", "Konuşma ritmi", "Claude Code", "Yerel"):
        w = int(d.textlength(tag, font=ft)) + 36 * S
        d.rounded_rectangle((x, 196 * S, x + w, 230 * S), 17 * S, outline=BLUE, fill=PANEL, width=S)
        d.text((x + w / 2, 213 * S), tag, font=ft, fill=BLUE, anchor="mm")
        x += w + 12 * S
    d.text((124 * S, 262 * S), "Geliştirici: ", font=f("segoeui.ttf", 17), fill=DIM, anchor="lm")
    d.text((124 * S + d.textlength("Geliştirici: ", font=f("segoeui.ttf", 17)), 262 * S), "findaeth",
           font=f("segoeuib.ttf", 17), fill=BLUE, anchor="lm")
    im.resize((W, H), Image.LANCZOS).save(hedef)


if __name__ == "__main__":
    main(sys.argv[1])
