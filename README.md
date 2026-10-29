# Kasir Warung Pintar

Aplikasi desktop kasir (POS) untuk warung sederhana, toko kelontong, toko sembako, dan usaha ritel kecil. Dibangun dengan **Python + PySide6 (Qt Widgets)** dan **SQLite** sebagai database lokal — berjalan penuh di komputer **tanpa browser, tanpa server, tanpa internet**.

## Fitur Utama

| Modul | Keterangan |
|---|---|
| Dashboard | 8 kartu statistik (omzet, transaksi, HPP, laba kotor, pengeluaran, estimasi laba bersih, stok menipis/habis), grafik 7 hari & bulanan, daftar transaksi terbaru/terlaris/stok |
| Kasir | Cari nama/kode/barcode, keranjang, diskon, tunai & non-tunai (QRIS/debit/transfer/e-wallet), kembalian otomatis, anti klik ganda, struk, shortcut F2/F4/F8 |
| Data Barang | CRUD, kategori, satuan dasar + satuan alternatif (renteng/dus/konversi), impor & ekspor Excel, penyesuaian stok beralasan, riwayat stok & harga, pagination |
| Peringatan Stok | Stok menipis & habis otomatis, badge di sidebar & lonceng di header, saran jumlah beli ulang |
| Pembelian | Stok bertambah, **HPP rata-rata tertimbang bergerak**, alokasi diskon & biaya perolehan proporsional, status bayar, pembatalan tervalidasi |
| Pengeluaran | Kategori (listrik/air/internet/dll), filter tanggal, grafik per kategori, ekspor Excel |
| Riwayat & Retur | Filter periode/metode/status, detail transaksi, cetak ulang struk, retur sebagian (barang layak → masuk stok; rusak → tidak), pembatalan (pemilik) |
| Laporan | 15 jenis laporan + laba rugi sederhana, kartu ringkasan, grafik, ekspor **PDF (ReportLab)** & **Excel (OpenPyXL)** |
| Struk | Thermal 58/80 mm + simpan PDF, pratinjau sebelum cetak |
| Pengguna | Peran **Pemilik/Admin** & **Kasir** dengan hak akses, password hash **PBKDF2-SHA256** |
| Pengaturan | Identitas warung, tema terang/gelap, ukuran struk, backup manual & otomatis, info database |
| Backup | Mekanisme **SQLite backup API** (aman dari transaksi setengah jadi), validasi file, restore dengan cadangan keamanan otomatis |

## Rumus Keuangan (dihitung di lapisan bisnis)

```
Omzet Bersih   = Penjualan Bruto − Diskon − Retur Penjualan
HPP            = Snapshot HPP item terjual (rata-rata tertimbang bergerak)
Laba Kotor     = Omzet Bersih − HPP
Laba Bersih Ops= Laba Kotor − Total Biaya Operasional
Nilai Persediaan = Stok × HPP per satuan saat ini
```

- Pembelian stok **tidak** langsung menjadi biaya operasional; HPP diakui saat barang terjual.
- Snapshot HPP disimpan per item transaksi sehingga laporan masa lalu tidak berubah.
- Retur dengan barang layak jual mengurangi HPP; barang rusak tidak (menjadi kerugian).

## Instalasi

Butuh **Python 3.10+** (disarankan 3.11/3.12).

```bash
cd kasir-warung-pintar

# 1. (opsional tapi disarankan) buat virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2. pasang dependensi
pip install -r requirements.txt

# 3. jalankan aplikasi
python main.py
```

Saat pertama dijalankan, aplikasi otomatis: membuat database di folder data pengguna, menerapkan skema (migrasi), membuat pengguna bawaan, dan mengisi **data demo** (26 barang, transaksi 45 hari, pengeluaran) agar dashboard langsung hidup. Gunakan `python main.py --no-demo` untuk memulai kosong.

### Akun Bawaan

| Pengguna | Kata Sandi | Peran |
|---|---|---|
| `pemilik` | `owner123` | Pemilik/Admin — seluruh modul |
| `kasir` | `kasir123` | Kasir — penjualan, struk, riwayat |

> Segera ubah kata sandi di menu **Pengaturan → Pengguna**.

### Opsi Baris Perintah

```
python main.py --no-demo        # tanpa data demo
python main.py --seed-only      # isi data demo lalu keluar
python main.py --data-dir X     # folder data khusus
python main.py --db X           # path database khusus
python main.py --version
```

## Lokasi Penyimpanan Data

Database SQLite disimpan di **folder data aplikasi** (bukan folder instalasi, aman ditulis):

| OS | Lokasi |
|---|---|
| Windows | `%APPDATA%\Kasir Warung Pintar\kasir_warung.db` |
| Linux/macOS | `~/.local/share/kasir-warung-pintar/kasir_warung.db` |

Folder `backups/`, `exports/`, `receipts/`, dan `logs/` dibuat di sebelahnya. **Database lama tidak pernah ditimpa** saat aplikasi diperbarui; skema dimutakhirkan lewat migrasi versi (`migrations/versions`).

## Cara Pakai Singkat

1. **Masuk** dengan akun pemilik atau kasir.
2. **Data Barang → Tambah** untuk mengisi barang (atau **Impor Excel**; gunakan tombol Ekspor sebagai contoh format).
3. **Pembelian Barang** saat restok — stok & HPP terhitung otomatis.
4. **Kasir**: klik `+` pada barang / ketik kode lalu Enter → keranjang → **Proses Pembayaran (F4)** → pilih metode → uang tunai & kembalian otomatis → struk tampil untuk dicetak/disimpan PDF.
5. **Dashboard/Laporan** memantau omzet, laba, dan stok setiap saat.
6. **Pengaturan → Backup & Pemulihan**: backup manual, aktifkan backup otomatis, pulihkan dari file.

### Shortcut Kasir

| Tombol | Fungsi |
|---|---|
| `F2` | Fokus ke pencarian barang |
| `F4` | Buka dialog pembayaran |
| `F8` | Kosongkan keranjang (dengan konfirmasi) |
| `Esc` | Tutup dialog (tidak pernah membuang data tanpa konfirmasi) |
| `Enter` | Tambah cepat barang dari hasil pencarian |

## Pengujian

```bash
python -m pytest tests/ -q
```

54 pengujian mencakup: penjualan tanpa member, multi barang, diskon & kembalian, pengurangan stok, stok tidak cukup (atomik), HPP rata-rata bergerak & snapshot, alokasi diskon pembelian, pembatalan pembelian, pengeluaran, retur (masuk/tanpa stok, refund proporsional), peringatan stok, nilai persediaan, 15 laporan + konsistensi dashboard=laporan, ekspor PDF/Excel, backup/restore, struk 58/80 mm & PDF, hak akses peran, konversi satuan, data tetap tersimpan setelah ditutup, dan migrasi idempoten.

## Versi Android (APK) untuk Tablet 8 Inci

Aplikasi ini punya **versi Android native (KivyMD)** di paket `mobile/` — mesin bisnis, database SQLite, rumus **HPP rata-rata tertimbang bergerak**, laba, retur, dan backup **identik dengan desktop**. Satu basis kode: `main.py` otomatis mendeteksi platform (desktop → PySide6, Android → KivyMD). Bisa pula dicoba di desktop dengan `KASIR_UI=mobile python main.py`.

**Layar mobile (dioptimalkan sentuh, landscape, tablet 8")**:

| Layar | Isi |
|---|---|
| Login | Akun pemilik/kasir, tombol *Muat Data Demo* |
| Dashboard | Kartu omzet/transaksi/laba, grafik 7 hari, barang terlaris, stok menipis |
| Kasir | Cari + filter kategori, katalog kartu sentuh, keranjang +/−, diskon |
| Pembayaran | Tunai & non-tunai (QRIS/debit/transfer/e-wallet), tombol uang cepat, kembalian otomatis, **Bagikan Struk** (share sheet Android) |
| Barang / Pembelian / Pengeluaran / Riwayat+Retur / Laporan / Pengaturan | CRUD penuh + backup & restore + pengguna + tema |

### Cara Mendapatkan APK

**Opsi A — GitHub Actions (tanpa instalasi apa pun, disarankan):**

1. Unggah folder proyek ke repositori GitHub.
2. Buka tab **Actions → Build APK Android → Run workflow**.
3. Tunggu ± 20–40 menit, lalu unduh artefak **KasirWarungPintar-APK** (file `.apk`).

**Opsi B — Build sendiri di Linux/WSL2:**

```bash
# prasyarat: Python 3.10/3.11, openjdk-17, autoconf/automake/libtool, pkg-config
pip install buildozer cython==0.29.36

cd kasir-warung-pintar
buildozer android debug        # pertama kali mengunduh SDK/NDK (± 3–5 GB)
# hasil: bin/kasirwarungpintar-1.0.0-arm64-v8a-debug.apk
```

Pasang di tablet: salin APK → buka file → izinkan "Instal aplikasi dari sumber tidak dikenal" → selesai. Di Windows gunakan **WSL2 Ubuntu** (buildozer tidak berjalan di Windows native).

**Data di Android** tersimpan di penyimpanan internal aplikasi (`user_data_dir`) — database, backup, dan struk tidak hilang saat aplikasi ditutup. Login pertama: `pemilik` / `owner123` (segera ganti di Pengaturan). Pengujian mobile dapat dijalankan headless: `xvfb-run -a python tests/mobile_smoke.py` (mencetak `=== MOBILE SMOKE OK ===`).

> Catatan teknis: KivyMD 2.0.0 dipilih agar konsisten teruji; widget yang tidak stabil (MDListItem, MDSnackbar, MDDatePicker, MDFab) digantikan komponen internal `mobile/ui_kit.py` (ListRow, toast, chips periode).

## Membangun Executable Windows (.exe)

Jalankan **di komputer Windows** (PyInstaller tidak membuat .exe lintas OS):

```bat
:: 1. siapkan environment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

:: 2. build
pyinstaller kasir_warung.spec --noconfirm --clean
```

Hasil: `dist\KasirWarungPintar.exe` (single-file, tanpa konsol). Atau cukup jalankan `scripts\build_exe.bat`. Aset (`assets/`) ikut terbungkus melalui spesifikasi; database tetap dibuat di folder data pengguna saat aplikasi pertama dijalankan.

## Struktur Proyek

```
kasir-warung-pintar/
├── main.py                  # titik masuk (dispatcher desktop/Android)
├── requirements.txt         # dependensi desktop
├── requirements-mobile.txt  # dependensi Android (via Buildozer)
├── kasir_warung.spec        # build PyInstaller (exe Windows)
├── buildozer.spec           # build APK Android
├── mobile/                  # APLIKASI ANDROID (KivyMD)
│   ├── app.py               # MobileKasirApp + pabrik layar
│   ├── db_boot.py           # bootstrap database di penyimpanan Android
│   ├── platform_tools.py    # share struk, deteksi Android, layar tetap nyala
│   ├── theme.py / ui_kit.py # palet navy + komponen sentuh (kartu, grafik, dialog)
│   └── screens/             # login, dashboard, kasir, pembayaran, barang,
│                            # pembelian, pengeluaran, riwayat+retur, laporan, pengaturan
├── mobile_assets/           # ikon & presplash APK
├── .github/workflows/       # build APK otomatis (GitHub Actions)
├── app/                     # MESIN BISNIS BERSAMA (dipakai desktop & mobile)
│   ├── core/                # config, konstanta, exception, tema, sinyal, AppContext
│   ├── database/            # engine SQLite, migrasi
│   ├── models/              # 18 tabel SQLAlchemy (ORM)
│   ├── repositories/        # lapisan akses data
│   ├── services/            # logika bisnis (penjualan, HPP, laba, retur, backup...)
│   ├── views/               # halaman GUI desktop (dashboard, kasir, laporan, ...)
│   ├── dialogs/             # dialog desktop (pembayaran, produk, retur, struk, ...)
│   ├── widgets/             # komponen UI desktop (sidebar, header, kartu, grafik)
│   ├── reports/             # ekspor Excel/PDF + penyusun struk
│   ├── printing/            # cetak thermal & PDF struk (desktop)
│   └── utils/               # format rupiah, tanggal, validasi, keamanan, ikon
├── assets/
│   ├── icons/               # ikon SVG (desktop)
│   └── styles/              # tema QSS terang & gelap (desktop)
├── migrations/versions/     # migrasi skema bertahap
├── tests/                   # 54 pytest + mobile_smoke (UI Android)
├── scripts/                 # seed data demo, build exe, generator ikon
└── backups/                 # lokasi backup default
```

## Catatan Teknis

- **Arsitektur 3 lapis**: `views (UI)` → `services (bisnis)` → `repositories/models (data)`. Semua perhitungan uang berada di services, bukan di form.
- **Transaksi atomik**: penjualan, pembelian, retur, dan pembatalan dibungkus satu transaksi database — kegagalan validasi tidak menyisakan data parsial.
- **Foreign key & WAL** SQLite diaktifkan otomatis pada setiap koneksi; index pada kolom pencarian panas.
- **Pencegahan transaksi ganda**: tombol proses dikunci saat menyimpan + validasi stok ulang di dalam transaksi.
- **Hak akses**: menu pembelian/pengeluaran/laporan/pengaturan disembunyikan untuk kasir; layanan juga memvalidasi peran (bukan hanya UI).
- Log aplikasi: `logs/kasir_warung.log` (berotasi 5 × 1 MB).
