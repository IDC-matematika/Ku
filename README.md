# IDC Kids — interaktiv daftar

IDC Kids (3–4 yosh) ish daftari asosidagi interaktiv mashqlar va yechimlar.

**Sayt:** https://idc-matematika.github.io/Ku/

| Bob | Topshiriqlar | Yechimlar |
| --- | --- | --- |
| 1. Boğ va mevalar | [boq-va-mevalar/](https://idc-matematika.github.io/Ku/boq-va-mevalar/) | [yechimlar](https://idc-matematika.github.io/Ku/boq-va-mevalar/yechimlar.html) |

## Audio («Tinglang» tugmasi)

Har bet uchun o'zbekcha ovozli yozuv qo'shish mumkin. Fayllarni `boq-va-mevalar/audio/` papkasiga
`p8.mp3`, `p9.mp3`, … `p28.mp3` nomlari bilan qo'ying (bet raqami bo'yicha). Fayl bor betlarda
sarlavhada «Tinglang» tugmasi o'zi paydo bo'ladi; fayl yo'q betlarda tugma ko'rinmaydi.

## Qanday ishlaydi

- `boq-va-mevalar/` — bob sahifalari (Claude Artifact formatida) va rasmlar.
- `site/index.html` — saytning bosh sahifasi.
- `scripts/build_site.py` — sahifalarni to'liq HTML hujjatga o'rab, `_site/` papkasiga yig'adi.
- `.github/workflows/pages.yml` — asosiy (default) branchga har push qilinganda saytni yig'ib, GitHub Pages'ga joylaydi.

Lokal tekshirish:

```bash
python3 scripts/build_site.py _site && python3 -m http.server -d _site 8000
```

Bir martalik sozlash: repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
