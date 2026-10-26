# 🩺 Muammolarni hal qilish

## Sonos ro'yxatda ko'rinmayapti

Chiqish ro'yxatida faqat **Music Assistant** `media_player` entity'lari
ko'rinadi. HA'ning o'z Sonos integratsiyasi entity'si (`media_player.zal` kabi)
u yerda chiqmaydi — bu to'g'ri, chunki `music_assistant.play_media` faqat MA
entity bilan ishlaydi.

**Yechim:** Music Assistant → **Settings → Providers → Add provider → Sonos**
(eski S1 tizim uchun **Sonos S1**). Sonos MA'da player bo'lib chiqqach, HA'da
uning MA entity'si paydo bo'ladi.

---

## Qo'shiq faqat Alice'dan chiqadi, Sonos jim ("The provider is currently unavailable")

Belgilari: Sonos ovozi o'zgarmaydi, Alice pasaymaydi, **Sozlamalar → Repairs**da
«Music Assistant qo'shiqni Sonos'da chala olmadi» chiqadi.

Sabab: Music Assistant'da **Yandex Music provayderi qo'shilmagan** (yoki
ishlamayapti). Integratsiya trekni `yandex_music://track/<id>` ko'rinishida
MA'ga beradi — provayder bo'lmasa, MA uni ocha olmaydi.

**Yechim:** Music Assistant → Settings → Music sources → «Add a music source» →
**Yandex Music** → Yandex hisobingizga kiring. Keyin Alice'da qo'shiqni qayta
qo'ying — Repairs ogohlantirishi o'zi yo'qoladi.

---

## Sonos'da pauza qildim — Alice ham to'xtadi

Bu ataylab qilingan: **«Sonos'dagi pauzani Alice'ga ham qo'llash»**. Aks holda
jim turgan Alice o'zi chalishda davom etib, keyingi trekda Sonos'ni yana yoqib
yuborardi. Sonos'da **Play** bossangiz — Alice ham davom etadi; yoki
"Alisa, prodolzhi" desangiz — musiqa Sonos'ga qaytadan uzatiladi.

Kerak bo'lmasa: **Configure → «Sonos'dagi pauzani Alice'ga ham qo'llash»** ni o'chiring.

---

## Sonos Amp / Arc / Beam'da televizor ko'rayotganda musiqa yoqilib ketdi

Alice'da musiqa boshlansa, integratsiya Sonos'ni televizor kirishidan musiqaga
o'tkazadi. Televizor ko'rayotganda **«Sinxron» switch**ni o'chirib qo'ying
(yoki TV yoqilganda shu switchni o'chiradigan avtomatika qiling).

---

## Bir nechta Sonos guruhlanmayapti / xonalar orasida farq bor

- Hamma Sonos **bitta** Music Assistant Sonos provayderi orqali qo'shilgan
  bo'lsin. Sonos + Arylic/AirPlay aralash bo'lsa — MA'da **Universal Group**
  yarating va integratsiyada o'sha bitta guruh entity'sini tanlang.
- Logda `are >2.5s out of sync` ogohlantirishi chiqsa: **Configure →
  «Har bir chiqishni alohida seek qilish»** ni yoqing.
- Guruh vaqt o'tib buzilsa: **«Har trekda qayta guruhlash»** ni yoqing.

---

## Sonos Alice'dan orqada / oldinda eshitiladi

[`TUNING.md`](TUNING.md) → «Sinxron offset». Sonos orqada bo'lsa offsetni
oshiring, oldinda bo'lsa kamaytiring.

---

## Sonos doim 0:00 dan boshlanadi yoki seekda stream uziladi

Sonos'da odatda bo'lmaydi. Agar shunday bo'lsa: **Configure → «Seekni o'tkazib
yuborish»** ni yoqing. Trek 0:00 dan boshlanadi, sinxron faqat offset bilan
taxminiy bo'ladi, lekin stream uzilmaydi.

---

## Alice 0 ga tushganda pauza bo'lib qoladi

Ba'zi Yandex firmware'larida `volume = 0` pauzani anglatadi.
**Alice yakuniy ovozi** ni `0.01` qiling.

---

## "Alisa, tishe" ishlamaydi, "gromche" ishlaydi

**Alice yakuniy ovozi** 0 bo'lsa, Alice 0 dan pastga tusha olmaydi va
"pasaytir" sezilmaydi. **Alice yakuniy ovozi** ni `0.05` qiling.

---

## Logni qanday ko'rish

`configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.alice_sonos_sync: debug
```

Har bir muhim Alice o'zgarishi, handoff/stop qadamlari va xonalar pozitsiyasi
logga yoziladi. «Sinxron» switch'ning `last_run` atributi oxirgi ishni ko'rsatadi
(`handoff`, `smooth_stop`, `follow_pause`, `follow_resume`, `handoff_failed`).
