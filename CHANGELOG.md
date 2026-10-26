# Changelog

Barcha muhim o'zgarishlar shu faylda qayd etiladi.
Format [Keep a Changelog](https://keepachangelog.com/) asosida.

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
