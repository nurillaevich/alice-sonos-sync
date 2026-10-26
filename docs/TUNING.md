# 🎚 Tuning qo'llanmasi

Bu yerda har bir sozlamani qanday his bilan moslash kerakligi tushuntirilgan.
Eng ko'p ta'sir qiladigan uchta narsa: **Sinxron offset**, **Sonos head-start**,
**Crossfade qadamlari**. Hammasi integratsiya kartasidagi **Configure** tugmasida.

> Standart qiymatlar boshlang'ich nuqta. Sonos'ning kechikishi uy tarmog'i va
> Music Assistant serveriga bog'liq — birinchi ishga tushirishda shu qo'llanma
> bo'yicha bir marta moslab oling.

---

## 1. Sinxron offset (soniya) — eng muhim

Sonos Alice bilan **bir xil sekunddan** chiqishi uchun. Seek qilinganda Sonos
biroz buferlanadi, shuning uchun unga "oldinroq" pozitsiya berib, vaqt
yo'qotishini qoplaymiz.

| Belgisi | Yechim |
|---|---|
| Sonos Alice'dan **orqada** (kechroq) eshitiladi | offset'ni **oshiring** (mas. 5 → 6.5) |
| Sonos Alice'dan **oldinda** (ertaroq) | offset'ni **kamaytiring** (mas. 5 → 3.5) |
| Har safar har xil | tarmoq beqaror — `Timeout: seekdan keyin kutish` ni 8 ga oshirib ko'ring |

> Aniq moslash uchun **Alice yakuniy ovozi** ni vaqtincha `0.3` qiling (Alice
> jim bo'lmasin), bir trekni qo'ying, ikkalasini yonma-yon eshiting va offsetni
> 0.5s qadam bilan surib boring. Tayyor bo'lgach `0` ga qaytaring.

---

## 2. Sonos head-start (ms)

Har crossfade qadamida **avval Sonos ko'tariladi**, keyin shu `head-start`
millisekunddan **keyin** Alice tushadi. Bu Sonos'ning buyruq qabul qilish
kechikishini yopadi — quloqqa Sonos doim biroz oldinda eshitiladi.

| Belgisi | Yechim |
|---|---|
| O'tishda "teshik" bor (ikkalasi ham bir lahza past) | **oshiring** → 450, 550 ms |
| O'tish juda cho'zilyapti | **kamaytiring** → 250, 200 ms |

---

## 3. Crossfade qadamlari

| Qiymat | Natija |
|---|---|
| Kam (6–8) | Tez, lekin pog'onalar sezilarli |
| O'rta (12) | Muvozanat (tavsiya) |
| Ko'p (18–24) | Juda silliq, lekin sekinroq |

**O'tish davomiyligi (taxminan):** `qadamlar × (head-start + Alice pauzasi)`.
Mas. `12 × (350 + 180) ms ≈ 6.4 soniya`.

---

## 4. Ovoz darajalari

- **Sonos boshlang'ich ovozi (0.05):** 0 emas, 5% — 0 dan boshlansa birinchi
  qadam juda sezilarli sakraydi.
- **Sonos yakuniy ovozi (0.25):** Sonos Amp / Five / Arc kuchli, shuning uchun
  standart past. Xonangizga qarab 0.20–0.45. Avval pastroqdan boshlang.
- **Alice yakuniy ovozi (0):** to'liq jim. Station 0 da pauza qilsa — **0.01**.
  "Pasaytir" ovoz buyrug'i ishlashi uchun **0.05** qiling.

---

## 5. To'xtash

- **Sonos pasayish chegarasi (0.01):** pauzadan oldingi eng past ovoz.
- **To'xtagach Sonos ovozini qaytarish (✅):** pauzadan keyin Sonos pasayishdan
  oldingi ovozga qaytadi. O'chirsangiz — Sonos 1% da qoladi.
- **Alice qaytariladigan ovoz (0.5):** odatdagi Alice ovozingiz.
- **Qadamlar (10) × kutish (200 ms) = 2 s** pasayish.
- **To'xtashni tasdiqlash kechikishi (1.0 s):** ovozli buyruqlaringiz uzun bo'lsa
  (mas. "ob-havo qanaqa") 2–3 s qiling.

---

## Tavsiya etilgan startlar

| Vaziyat | Sinxron offset | Head-start | Qadamlar |
|---|---|---|---|
| Tez, simli tarmoq (Sonos Ethernet'da) | 4.0 | 300 | 10 |
| Muvozanat (standart) | 5.0 | 350 | 12 |
| Sekin/beqaror Wi-Fi | 6.5 | 550 | 14 |
