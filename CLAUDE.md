# Dublaj Prompter: Claude Code talimatları

Bu depo, İngilizce YouTube videolarına Türkçe seslendirme yapmak için yerel bir prompter içerir. Kullanıcı genelde yalnızca bir YouTube linki verir. Yanıtları Türkçe ver. Teknik terimleri (PLC, LiDAR, Modbus vb.) çevirme. Kısa ve doğrudan yaz.

## Kullanıcı link verince
1. Gereksinimleri kontrol et (`README.md`). Eksik paket varsa kurmadan önce kullanıcıya söyle.
2. `python hazirla.py "<link>"` çalıştır. Çıktı `veri/<video-id>/en.txt`, `en.json` ve karaoke zamanları için `ritim.json`.
3. `en.txt` dosyasını aşağıdaki kurallarla Türkçeye çevirip `veri/<video-id>/prompter.txt` olarak yaz. Uzun metni sohbete dökme, dosyaya yaz ve kısa özet ver.
4. Çeviriden sonra kontrol et: metinde `/` karakteri yok mu, blok başına kelime sayısı süreye sığıyor mu (yaklaşık 2,5 kelime/sn üstü bloğu kısalt, bilgi atma).
5. Kullanıcıya şunu söyle: PowerShell'de `.\baslat.bat <video-id>`. Eski video ve prompter sekmelerini kapatmasını hatırlat.

## Çeviri kuralları
- Sıfır bilgi kaybı: tek bir teknik detayı, örneği veya cümleyi atlama. Özet çıkarma.
- Anlam sırası İngilizceyle aynı kalsın (hoca çevirinin sadık olduğunu görebilsin), ama cümleler doğal konuşma Türkçesi olsun. Motamot çeviri yapma, devrik cümle kurma.
- Cümleleri nefes yerlerinden bölüp alt alta kısa satırlar yaz.
- Cümle içinde `/` ve okuma akışını bozacak semboller kullanma.
- YouTube otomatik altyazı/Whisper hatalarını bağlama göre düzelt (örn. "zuk" yerine Zoox). Yabancı özel isimlerin ve kısaltmaların okunuşunu ilk geçtikleri yerde parantezle yaz: `Waymo (Veymo)`, `LiDAR (Laydar)`.
- Teknik terimleri doğru karşılıklarıyla kullan (platooning: araç katarı, sensor fusion: sensör birleştirme, redundancy: yedeklilik).
- Özel isimleri, sayıları ve ortak teknik terimleri (Waymo, NVIDIA, 2021, LiDAR) Türkçe metinde İngilizce yazımıyla bırak. Prompter bunları konuşmacının söylediği İngilizce kelimeye çapalar ve karaoke senkronu iyileşir. Sayıları sözcükle yazmak da (dört) eşleşir.
- Videodaki reklam/sponsor bölümünü atlama, ama başlığına `SPONSOR BÖLÜMÜ BAŞLIYOR - İSTERSEN ATLA` yaz. Konuşmacının esprisi ya da belirsiz duyulan yer varsa parantez içinde bırak ve kullanıcıya doğrulamasını söyle.

## prompter.txt biçimi
Örnek: `ornek/prompter.txt`.
- Her blok `[m:ss]` ya da `[m:ss - NOT]` ile başlar. Zaman İngilizce transkriptteki ilk segmentin saniyesidir. Bloklar yaklaşık 4-15 saniye olsun.
- Sahne notu gerekiyorsa köşeli parantez içinde büyük harfle: `[1:22 - SAHNE GEÇİŞİ - 2 SANİYE BEKLE]`.
- `.` tek başına satır boşluk bırakır. Bölüm geçişlerinde kullan.
- Her bloğun başına, adamın o blokta ilk ve son söylediği İngilizce sözlerden 3-4 kelimelik bir ipucu satırı yaz: `~ "ilk sözler" ... "son sözler"`. Bu satır okunacak metinden ayrıdır.

## Değiştirirken
- `video.html` (YouTube oynatıcı, zamanı yayar) ve `prompter.html` (metni kaydırır, kumanda gönderir) `BroadcastChannel("dublaj")` ile konuşur. Mesajlar video ID'si (`v`) taşır, prompter yalnızca kendi videosunu dinler.
- `prompter.html` içinde `blokPlanla` (blok zamanlaması), `hizala` (Türkçe ve İngilizce kelime çapaları), `konusmaEgrisi` ve `konusmaIlerleme` (konuşma ritmi) var. `ritim.json` yoksa hece ağırlığına düşer. Mantığı değiştirirsen durak, çapa ve yedek durumlarını sentetik bir örnekle `node` ile test et.
- Değişiklikten sonra inline script'in sözdizimini `node --check` ile kontrol et. Tarayıcıda denemeden "çalışıyor" deme.

## Telif ve gizlilik
- Yalnızca kullanıcının kendi videosu ya da dublaj izni olan videolarla çalış. Yayımlamadan önce izin gerektiğini hatırlat.
- `veri/` ve `inceleme/` klasörlerini commit etme (`.gitignore`'da).
