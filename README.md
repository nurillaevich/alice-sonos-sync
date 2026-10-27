# 🎶 Alice ↔ Sonos — Smooth Sync

> Yandex Station (**Alice**) da boshlangan musiqani **Music Assistant** orqali
> **Sonos** kolonka / kuchaytirgichga (Sonos Amp, Port, Era, Five, Arc, Beam…)
> *xuddi shu sekunddan*, yumshoq crossfade bilan uzatadigan va to'xtaganda yana
> yumshoq qaytaradigan Home Assistant integratsiyasi (+ blueprintlar).

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
![type](https://img.shields.io/badge/type-Integration%20%2B%20Blueprints-blue)
![ha](https://img.shields.io/badge/Home%20Assistant-2024.12%2B-41BDF5)
![license](https://img.shields.io/badge/license-MIT-green)

English version: [`README.en.md`](README.en.md)

Bu [alice-arylic-sync](https://github.com/nurillaevich/alice-arylic-sync) ning
**Sonos** uchun moslangan versiyasi: bir xil sinxron dvigateli, lekin Sonos
nomlari, Sonos uchun standart qiymatlar va Sonos'ga xos ikki qo'shimcha
imkoniyat bilan.

---

## 📌 Bu nima?

Yandex Station ovozi unchalik kuchli emas. Ko'pchilik Alice bilan **boshqarib**,
ovozni esa **Sonos** orqali chiqarishni xohlaydi. Muammo — ikki qurilma sinxron
emas: biri oldinda, biri orqada yangraydi yoki ikkalasi bir vaqtda gapirib,
"echo" bo'ladi.

| Holat | Nima bo'ladi |
|---|---|
| **Alice'da trek boshlandi** | O'sha trek Sonos'da aynan shu sekunddan qo'yiladi va **navbatma-navbat** crossfade bo'ladi: Sonos bir pog'ona ko'tariladi → Alice bir pog'ona tushadi → ... Oxirida Alice **0** (jim), Sonos **to'liq** ovoz. |
| **Alice'da musiqa to'xtadi** | Sonos yumshoq pasayib pauza bo'ladi, keyin Sonos ovozi **avvalgi darajaga qaytariladi**; Alice ovozi belgilangan darajaga (mas. **50%**) qaytadi. |
| **Sonos'da pauza bosildi** (ilova yoki tugma) | Alice ham pauza bo'ladi va ovozi qaytadi. Sonos'da yana **Play** bossangiz — Alice ham jim holda davom etadi. |
| **"Alisa, gromche / tishe"** | Handoff'dan keyin ovoz buyrug'i Alice'ga emas, **Sonos'ga** qo'llanadi. |
| **Sonos'da telefondan AirPlay (yoki TV / Line-in) chalayapti** | Alice pauza/stop qilinsa, Sonos'ga **tegilmaydi** — ikkalasi o'z holicha davom etadi. Alice yangi qo'shiq boshlasa — qo'shiq Sonos'ga uzatiladi. |

---

## 🆕 Sonos'ga xos imkoniyatlar

| Imkoniyat | Standart | Nima uchun |
|---|---|---|
| **Sonos'dagi pauzani Alice'ga ham qo'llash** | ✅ yoqiq | Sonos ilovasi yoki Sonos'ning o'z tugmasi bilan pauza qilsangiz, jim turgan Alice o'zi chalishda davom etmaydi va keyingi trekda Sonos'ni "o'zi" yoqib yubormaydi. Trek tabiiy tugashi (`idle`) pauza hisoblanmaydi. |
| **To'xtagach Sonos ovozini qaytarish** | ✅ yoqiq | To'xtash paytida Sonos 1% gacha pasayadi. Shu imkoniyat bo'lmasa, Sonos ilovasidan keyingi ijro 1% dan boshlanardi. Endi pauzadan keyin ovoz pasayishdan oldingi darajaga qaytadi. |
| **Sonos yakuniy ovozi 25%** | `0.25` | Sonos Amp / Five / Arc kuchli — standart past. **Configure**'da o'zingizga moslang. |

Qolgan hammasi asl integratsiyadagidek: multi-room, **Sonos guruhi** knopkasi,
ovoz buyrug'ini yo'naltirish, ovozli buyruqdagi "lahzalik to'xtash"ni sezish,
Music Assistant xato bersa **Repairs**'da ogohlantirish.

---

## 🆚 Alice va Sonos — qaysi entity'ni tanlash kerak

| | **Alice (Yandex Station)** | **Sonos (Music Assistant)** |
|---|---|---|
| **Roli** | MANBA + boshqaruv | CHIQISH |
| **Qaysi entity** | `media_player.yandex_station_...` | Sonos'ning **Music Assistant'dagi** `media_player` entity'si |
| **Diqqat** | — | ❗ HA'ning o'z **Sonos** integratsiyasi entity'si emas, aynan **Music Assistant** entity'si bo'lsin — chunki `music_assistant.play_media` faqat MA entity bilan ishlaydi. Integratsiya ro'yxatida faqat MA entity'lari ko'rinadi, adashib bo'lmaydi. |

---

## ✅ Talablar

1. **Home Assistant** 2024.12+ (integratsiya uchun; blueprintlarga 2024.10 yetadi).
2. **[Music Assistant](https://music-assistant.io/)** integratsiyasi o'rnatilgan.
3. **Sonos** Music Assistant'ga qo'shilgan: Music Assistant → **Settings → Providers →
   Add provider → Sonos** (S2 tizimi uchun; eski S1 kolonkalar uchun **Sonos S1**).
   Shundan keyin HA'da Sonos'ning Music Assistant `media_player` entity'si paydo bo'ladi.
4. **Yandex Station** Home Assistant'ga ulangan (mas.
   [AlexxIT/YandexStation](https://github.com/AlexxIT/YandexStation)) va uning
   `media_player` entity'si `media_content_id`, `media_position` atributlarini beradi.
5. Music Assistant'da **Yandex Music** provayderi qo'shilgan — integratsiya trekni
   `yandex_music://track/<id>` ko'rinishida beradi. Boshqa provayder ishlatsangiz —
   **Configure → Trek URI prefiksi** ni o'zgartiring.

---

## 🚀 O'rnatish

### 1-usul — Integratsiya (HACS orqali, tavsiya etiladi) ⭐

1. **HACS → ⋮ (yuqori o'ng) → Custom repositories** ni oching.
2. **Repository:** `https://github.com/nurillaevich/alice-sonos-sync`
   · **Type:** `Integration` → **Add**.
3. HACS ro'yxatidan **Alice ↔ Sonos Sync** ni topib **Download** qiling,
   so'ng Home Assistant'ni qayta ishga tushiring.
4. **Settings → Devices & Services → Add Integration** → "**Alice ↔ Sonos Sync**".
5. Menyudan **«🎵 Alice → Sonos juftlik»** ni tanlang va kolonkalarni belgilang:
   - **Alice (Yandex Station)** — manba (ro'yxatda faqat Yandex stansiyalar);
   - **Sonos (Music Assistant)** — chiqish: **bitta yoki bir nechta** Sonos.
     Bir nechta tanlasangiz — **multi-room**: hammasi Sonos guruhiga birlashib,
     bir xil musiqani sinxron chaladi (birinchi tanlangani — yetakchi).
6. Tamom. **Barcha sozlamalar** integratsiya kartasidagi **Configure** tugmasida.

> HACS'siz qo'lda: `custom_components/alice_sonos_sync/` papkasini HA'dagi
> `config/custom_components/` ichiga nusxalang va HA'ni qayta ishga tushiring.

> 💡 Har bir juftlik uchun **Sinxron** switch yaratiladi — sinxronlashni
> vaqtincha o'chirib qo'yish uchun (mas. Sonos Amp/Arc'da televizor ko'rayotganda).

> ⚠️ Bir Alice uchun **alice-arylic-sync** va **alice-sonos-sync**'ni bir vaqtda
> ishlatmang — ikkalasi ham Alice ovozini boshqaradi va bir-biriga xalaqit beradi.

### 2-usul — Blueprint (YAML avtomatika)

| Blueprint | Import |
|---|---|
| **Smooth Handoff (Start)** | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fnurillaevich%2Falice-sonos-sync%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Falice_sonos%2Falice_sonos_handoff_start.yaml) |
| **Smooth Stop & Restore** | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fnurillaevich%2Falice-sonos-sync%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Falice_sonos%2Falice_sonos_smooth_stop.yaml) |

Yoki **Settings → Automations & Scenes → Blueprints → Import Blueprint** va:

```
https://github.com/nurillaevich/alice-sonos-sync/blob/main/blueprints/automation/alice_sonos/alice_sonos_handoff_start.yaml
```
```
https://github.com/nurillaevich/alice-sonos-sync/blob/main/blueprints/automation/alice_sonos/alice_sonos_smooth_stop.yaml
```

> Blueprintlarda «Sonos'dagi pauzani Alice'ga qo'llash», multi-room va ovoz
> buyrug'ini yo'naltirish **yo'q** — ular faqat integratsiyada.
> Blueprint ishlatsangiz, integratsiyani o'rnatmang (har trek ikki marta uzatiladi).

---

## 🏠 Multi-room (bir nechta Sonos)

**1-yo'l (eng oson):** integratsiyada bir nechta Sonos tanlang. Musiqa
boshlanganda ular yetakchiga qo'shilib (`media_player.join`) Sonos'ning o'z
guruhiga aylanadi — namuna-aniq sinxron.

**2-yo'l:** Music Assistant'da doimiy guruh yarating va integratsiyada o'sha
**guruh entity'sini** (bitta) tanlang.

> ⚠️ Hamma Sonos **bitta** Music Assistant Sonos provayderi orqali qo'shilgan
> bo'lsin. Sonos'ni boshqa turdagi kolonka (Arylic, AirPlay) bilan aralashtirsangiz,
> MA'da "Universal Group" yaratib, 2-yo'ldan foydalaning.

**👥 Sonos guruhi knopkasi:** integratsiya qo'shishda **«👥 Sonos guruhi»** ni
tanlasangiz, Alice'siz bitta **Guruh** switch paydo bo'ladi: **ON** — barcha
kolonkalar yetakchiga qo'shiladi, **OFF** — har biri mustaqil bo'ladi. Switch
haqiqiy holatni ko'rsatadi (Sonos ilovasida guruhlasangiz ham).

---

## ⚙️ Sozlamalar (Configure)

| Sozlama | Standart | Ma'nosi |
|---|---|---|
| **Sinxron offset (s)** | `5.0` | ⭐ Sonos'ni Alice bilan bir sekundga moslash |
| **Sonos head-start (ms)** | `350` | ⭐ Har qadamda Sonos Alice'dan qancha oldinda yursin |
| **Crossfade qadamlari** | `12` | Ko'p = silliq, kam = tez |
| **Sonos boshlang'ich / yakuniy ovozi** | `0.05` / `0.25` | Crossfade qayerdan qayergacha |
| **Alice yakuniy ovozi** | `0` | Alice qayergacha tushadi (0 = jim) |
| **To'xtash: Alice qaytariladigan ovoz** | `0.5` | To'xtagach Alice shu ovozga qaytadi |
| **To'xtashni tasdiqlash kechikishi (s)** | `1.0` | Ovozli buyruqdagi lahzalik to'xtashni haqiqiy to'xtashdan ajratadi |
| **Sonos'dagi pauzani Alice'ga ham qo'llash** | ✅ | Yuqoridagi jadvalga qarang |
| **To'xtagach Sonos ovozini qaytarish** | ✅ | Yuqoridagi jadvalga qarang |
| **Har trekda qayta guruhlash** | ❌ | Xonalar vaqt o'tib ajralib ketsa |
| **Har bir chiqishni alohida seek qilish** | ❌ | Kolonkalar bitta guruhga birlasha olmasa |
| **Seekni o'tkazib yuborish** | ❌ | Seekda stream uzilsa (Sonos'da odatda kerak emas) |
| **Alice ovoz buyrug'ini kolonkalarga yo'naltirish** | ✅ | "Gromche/tishe" → Sonos |
| **Trek URI prefiksi** | `yandex_music://track/` | Boshqa MA provayderi uchun o'zgartiring |

To'liq qo'llanma: [`docs/TUNING.md`](docs/TUNING.md) ·
Muammolar: [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

> **Holat:** v1.0.0 avtomatik testlar (pytest + Home Assistant) bilan tekshirilgan.
> Sinxron offset va head-start har bir uy tarmog'iga qarab farq qiladi — birinchi
> ishga tushirishda [`docs/TUNING.md`](docs/TUNING.md) bo'yicha moslab oling.

---

## 🔧 Qanday ishlaydi

1. Alice'da trek almashadi yoki ijro boshlanadi.
2. Bir nechta Sonos bo'lsa — ular yetakchiga guruhlanadi.
3. Sonos `floor` ovozga qo'yiladi, o'sha trek `music_assistant.play_media` bilan boshlanadi.
4. Sonos yangi trekka o'tguncha kutiladi.
5. Alice turgan sekund (`+ sync_offset`) hisoblanib, Sonos shu joyga `media_seek` qilinadi.
6. Navbatma-navbat crossfade: har qadam → **Sonos +** → head-start pauza → **Alice −**.
7. Oxirida Alice `end volume` (0), Sonos `target` ovozga ega bo'ladi.

---

## 📂 Repo tuzilishi

```
alice-sonos-sync/
├── custom_components/alice_sonos_sync/   # ⭐ Integratsiya (HACS: Integration)
│   ├── __init__.py / controller.py       #    sinxron dvigateli
│   ├── config_flow.py                    #    UI: kolonka tanlash + sozlamalar
│   ├── switch.py                         #    Sinxron / Guruh switch
│   └── manifest.json / strings.json / translations/
├── blueprints/automation/alice_sonos/    # Muqobil: blueprint variant
├── examples/                             # namuna (to'ldiriladigan) avtomatikalar
├── tests/                                # pytest + Home Assistant testlari
├── docs/ (TUNING.md, TROUBLESHOOTING.md)
├── .github/workflows/validate.yaml       # CI: yamllint + pytest + hassfest + HACS
└── hacs.json · CHANGELOG.md · LICENSE
```

---

## 📝 Litsenziya

MIT — [`LICENSE`](LICENSE).
