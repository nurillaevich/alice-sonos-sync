# Changelog

Barcha muhim o'zgarishlar shu faylda qayd etiladi.
Format [Keep a Changelog](https://keepachangelog.com/) asosida.

## [1.1.0] - 2026-10-27

### Qo'shildi
- **Music Assistant'siz ishlash.** Chiqish ro'yxatida endi **HA'ning o'z Sonos
  integratsiyasidagi kolonkalar** ham chiqadi. Shunday kolonka tanlansa,
  Alice chalayotgan trek YandexStation integratsiyasining o'z Yandex sessiyasi
  orqali olinadi (xuddi YandexStation'ning «стриминг музыки» funksiyasidagidek)
  va Sonos'ga to'g'ridan-to'g'ri stream qilinadi — Music Assistant ham,
  qo'shimcha Yandex login ham kerak emas. Seek (Alice turgan sekunddan
  boshlash) va crossfade avvalgidek ishlaydi. Music Assistant kolonkalari ham
  ro'yxatda qoladi (ular uchun MA'da Yandex Music kerak).
- Real holatdan: Music Assistant o'chirilgach, juftlik qo'shish oynasida
  kolonkalar ro'yxati bo'sh chiqardi («Нет доступных элементов»).

### Tuzatildi
- Integratsiya endi Sonos'da **faqat o'zi qo'ygan oqimni** to'xtatadi: uzatishdan
  keyin Sonos'da azan, AirPlay yoki TV chalinsa, Alice to'xtaganda ularga
  tegilmaydi (native Sonos AirPlay/TV'ni `x-sonos-vli:` / `x-sonos-htastream:`
  ko'rinishida ko'rsatadi — bular ham tanildi).
- Kolonka tarmoqda bo'lmagani uchun uzatish o'tkazib yuborilsa, keyingi
  to'xtashda Alice ovozi endi o'zgartirilmaydi (avval 50% ga qo'yilardi).

## [1.0.1] - 2026-10-27

### Tuzatildi
- **Alice pauza qilinganda Sonos'dagi boshqa ijro (telefondan AirPlay) ham
  pasaytirilib to'xtatilardi.** Real holatda ko'rildi: Music Assistant'da Yandex
  Music provayderi yo'qligi sababli birorta ham uzatish bo'lmagan, keyin
  telefondan Sonos'ga AirPlay qo'yilgan — Alice pauza qilinganda integratsiya
  o'sha AirPlay musiqasini 1% gacha tushirib pauza qilib qo'ygan. Endi:
  - to'xtash faqat integratsiya trekni haqiqatan **muvaffaqiyatli uzatgan**
    bo'lsa ishlaydi;
  - manbasi **AirPlay / TV / Line-in** bo'lgan kolonkaga tegilmaydi —
    Sonos'ni boshqa manba egallab olgan bo'lsa, u o'z holicha chalaveradi;
  - Sonos'dagi AirPlay pauzasi Alice'ni pauza qilmaydi.
- Uzatishdan keyin Sonos treki tugab `idle` bo'lgan yoki AirPlay egallagan
  bo'lsa, Alice to'xtaganda uning ovozi endi baribir qaytariladi (avval jim
  qolib ketardi).

### Tasdiqlandi (o'zgarmagan)
- Sonos'da AirPlay pauzada turganda Alice yangi qo'shiq boshlasa, qo'shiq
  Sonos'ga uzatiladi (test qo'shildi).

## [1.0.0] - 2026-10-26

Birinchi versiya — [alice-arylic-sync](https://github.com/nurillaevich/alice-arylic-sync)
1.6.4 ning **Sonos** uchun moslangan nusxasi.

### Qo'shildi
- **Alice → Sonos juftlik:** Alice'da boshlangan trek Music Assistant orqali
  Sonos'da xuddi shu sekunddan boshlanadi, navbatma-navbat crossfade bilan;
  to'xtaganda Sonos yumshoq pasayib pauza bo'ladi. Bir nechta Sonos —
  multi-room (Sonos guruhi).
- **Sonos'dagi pauzani Alice'ga ham qo'llash** (standart yoqiq): Sonos ilovasi
  yoki tugmasi bilan pauza qilinsa, Alice ham pauza bo'ladi va ovozi qaytadi;
  Sonos'da yana Play bosilsa, Alice jim holda davom etadi. Trek tabiiy tugashi
  (`idle`) va 1.5 s dan qisqa lahzalik pauza hisoblanmaydi; Sonos ilovasidan
  boshqa qo'shiq qo'yilsa, Alice qayta yoqilmaydi.
- **To'xtagach Sonos ovozini qaytarish** (standart yoqiq): pauzadan keyin Sonos
  ovozi pasayishdan oldingi darajaga qaytadi — Sonos ilovasidan keyingi ijro 1%
  dan boshlanmaydi. Faqat pauza haqiqatan amalga oshgan kolonkalarga qo'llanadi.
- **Sonos guruhi** knopkasi (Alice'siz, 2+ kolonkani bitta switch bilan ulash).
- Smooth Handoff / Smooth Stop blueprintlari (Stop'da Sonos ovozini qaytarish bilan),
  blueprint selektorlari faqat Yandex Station va Music Assistant entity'larini ko'rsatadi.
- pytest + Home Assistant testlari va CI'da ularni ishga tushirish.

### O'zgartirildi (alice-arylic-sync'ga nisbatan)
- Sonos yakuniy ovozi standarti `0.35` → **`0.25`** (Sonos Amp / Five / Arc kuchli).
- Integratsiya o'chirilganda faqat a'zo kolonkalar guruhdan chiqariladi
  (yetakchini `unjoin` qilish ba'zi MA provayderlarida `set_members` xatosini beradi).
