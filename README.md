# Dublaj Prompter

İngilizce YouTube videolarına Türkçe seslendirme yaparken kullanılan yerel prompter. Videonun zamanına bağlı kayar, videoyu prompter sayfasından durdurup ileri geri sarabilirsin.

Akış: YouTube linki, Whisper ile zaman damgalı İngilizce transkript, Türkçe prompter metni (`prompter.txt`), iki sekmeli yerel prompter sitesi.

## Edinme
GitHub sayfasında **Code**, ardından **Download ZIP** ile indir (GitHub hesabı gerekmez) ya da `git clone` kullan.

## Claude Code ile kullanım
Klasörü Claude Code'da aç (`claude`). `CLAUDE.md` talimatları otomatik yüklenir. Şunu yaz: "Şu videoyu hazırla: <YouTube linki>". Transkripti çıkarır, Türkçe prompter metnini yazar ve hangi komutu çalıştıracağını söyler.

## Gereksinimler (Windows)
- Python 3.10+
- Node.js (yt-dlp YouTube için JavaScript çalıştırıcısı olarak kullanır)
- ffmpeg: `winget install Gyan.FFmpeg`
- Python paketleri: `pip install faster-whisper yt-dlp pyyaml "av==16.1.0"`

`av` sürümünü 16.1.0'da tut. `faster-whisper` 1.2.1 ile `av` 19 uyumsuz.

## Kullanım
1. Transkript çıkar: `python hazirla.py "<youtube linki>"`. Çıktı `veri/<video-id>/en.txt`.
2. Transkripti Türkçeye çevir ve `veri/<video-id>/prompter.txt` olarak kaydet (bu depodaki `CLAUDE.md`, Claude Code ile bunu yapmanı sağlar).
3. PowerShell'de `.\baslat.bat <video-id>` çalıştır. İki sekme açılır: video sekmesi (Meet'e ya da kayda bunu paylaş) ve prompter sekmesi.
4. Prompter sekmesinde: düğmeler ve `Space`, `←`, `→` (Shift ile 10 sn) ile videoyu yönet. Bir satıra tıklayınca video o saniyeye atlar.

Eski video ve prompter sekmelerini yeni video açmadan önce kapat. Sunucu terminalde çalışır, kapatmak için `Ctrl+C`.

## prompter.txt biçimi
`ornek/prompter.txt` dosyasına bak. Kısaca:
- `[m:ss]` ya da `[m:ss - NOT]` yeni bloğu başlatır. Metin bloğun saniyesinden bir sonraki bloğa kadar yayılır.
- `.` tek başına satır: boşluk.
- `~ "ilk sözler" ... "son sözler"`: adamın bloğa başlarken ve bitirirken söylediği İngilizce sözler. Küçük, mavi ve okunmaz, yerini bulmak içindir. Üstteki "İng. ipucu" ile gizlenir.

## Notlar
- Yalnızca kendi videon ya da dublaj izni olan videolarla kullan. Üçüncü kişilerin videolarının transkriptini ve çevirisini depoya koyma (`veri/` bu yüzden `.gitignore`'da).
- Whisper Türkçe sesi İngilizceden kötü yazar. Transkripti çıkarmak için İngilizce videolar uygundur.
- Senkron tarayıcıda YouTube IFrame API'ye dayanır. Reklam çıkarsa zaman kayar. Tarayıcı, video sekmesine hiç tıklanmadan gelen "oynat" komutunu engelleyebilir, bu durumda videoyu bir kez elle başlat.
