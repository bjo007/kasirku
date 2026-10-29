# Panduan Upload ke GitHub & Build APK (Bahasa Indonesia)

Panduan ini menjawab: **"File mana yang harus di-upload ke GitHub?"** dan
**"Kok folder .github-nya hilang?"**

---

## 1. File yang harus di-upload: SEMUA isi folder proyek

Upload **seluruh isi folder `kasir-warung-pintar/`** (bukan hanya folder `mobile/`),
karena GitHub Actions butuh semua bagian ini untuk membuat APK:

| Item | Wajib? | Fungsi |
|---|---|---|
| `.github/workflows/build-apk.yml` | **WAJIB** | Resep build otomatis di server GitHub |
| `buildozer.spec` | **WAJIB** | Konfigurasi APK (nama, versi, ikon, dependensi) |
| `main.py` | **WAJIB** | Titik masuk aplikasi (deteksi Android otomatis) |
| `app/` | **WAJIB** | Mesin bisnis: HPP, laba, retur, backup, database |
| `migrations/` | **WAJIB** | Skema database |
| `mobile/` | **WAJIB** | Layar sentuh Android (KivyMD) |
| `mobile_assets/` | **WAJIB** | Ikon & splash screen APK |
| `requirements-mobile.txt` | Wajib | Daftar dependensi Android |
| `assets/`, `tests/`, `scripts/`, `requirements.txt`, `README.md`, `kasir_warung.spec`, `.gitignore` | Ikutkan saja | Untuk versi desktop & pengujian |

> Catatan: `data/`, `backups/`, `bin/`, `__pycache__/` **tidak perlu** —
> otomatis dibuat saat aplikasi berjalan, dan sudah diabaikan oleh `.gitignore`.

---

## 2. "Kok folder .github-nya hilang?" — TIDAK HILANG, hanya tersembunyi

Folder `.github` dan file `.gitignore` **diawali titik** → dianggap file/folder
**tersembunyi** oleh sistem operasi, sehingga tidak tampil di file manager secara default.

**Cara menampilkannya:**

- **Windows Explorer**: buka folder → tab **View / Tampilan** → centang **Hidden items / Item tersembunyi**. (Di Windows folder titik biasanya sudah terlihat.)
- **macOS Finder**: di dalam folder tekan **Cmd + Shift + .** (titik). Tekan lagi untuk sembunyikan.
- **File manager Android**: menu ⋮ → **Show hidden files / Tampilkan file tersembunyi**.
- **Linux (Nautilus/Files)**: tekan **Ctrl + H**.

Setelah tampil, pastikan di dalamnya ada: `.github/workflows/build-apk.yml`.

> Kalau Anda meng-unzip paket `kasir-warung-pintar.zip` versi lama (sebelum fitur
> Android ditambahkan), memang folder `.github`, `mobile/`, dan `mobile_assets/`
> belum ada. **Gunakan ZIP terbaru** dan unzip ulang.

---

## 3. Cara Upload — Pilih salah satu

### Cara A: Upload lewat browser (paling mudah, tanpa instal git)

1. Buka **https://github.com** → login → klik **+** (kanan atas) → **New repository**.
2. Isi nama repo, misal `kasir-warung-pintar` → pilih **Private** (disarankan) → klik **Create repository**.
3. Di halaman baru, klik link **uploading an existing file**.
4. Buka folder proyek yang sudah di-unzip, **tampilkan file tersembunyi** (lihat §2),
   lalu **blok SEMUA isi di dalamnya** (termasuk `.github`) → seret (drag & drop) ke area upload browser.
   - Windows: drag biasa — folder `.github` ikut terseret.
   - macOS: setelah Cmd+Shift+. , drag semua.
   - **Alternatif jika drag `.github` gagal**: klik **Add file → Create new file**,
     ketik nama `.github/workflows/build-apk.yml`, lalu tempel (paste) isinya dari
     file asli. Ulangi juga untuk `.gitignore` bila perlu.
5. Tunggu semua file terunggah (± 300 file, 1–2 menit) → tulis pesan commit (mis. `Kasir Warung Pintar`) → klik **Commit changes**.
6. **Verifikasi**: di halaman repo harus terlihat folder `.github`, `app`, `mobile`, `mobile_assets`, `migrations`, serta file `buildozer.spec` dan `main.py`.

### Cara B: Upload lewat perintah git (paling andal)

Install git dulu (git-scm.com), lalu di folder proyek jalankan satu per satu
(ganti `NAMAANDA` dengan username GitHub Anda):

```bash
cd kasir-warung-pintar
git init
git add .
git commit -m "Kasir Warung Pintar: desktop + Android"
git branch -M main
git remote add origin https://github.com/NAMAANDA/kasir-warung-pintar.git
git push -u origin main
```

Saat diminta login, gunakan **Personal Access Token** (bukan password) —
buat di GitHub: Settings → Developer settings → Personal access tokens → Generate (scope: `repo`).

---

## 4. Membuat APK di GitHub (gratis, tanpa komputer Linux)

1. Buka repo Anda di GitHub → tab **Actions**.
2. Jika muncul tombol kuning *"Workflows aren't being run on this forked repository"*,
   klik **I understand my workflows, go ahead and enable them**.
3. Di daftar kiri pilih **Build APK Android** → klik tombol **Run workflow** → **Run workflow** (konfirmasi).
4. Tunggu **± 20–40 menit** (build pertama mengunduh Android SDK/NDK di server GitHub).
5. Setelah titik hijau ✓ muncul, klik run tersebut → bagian bawah halaman ada
   **Artifacts** → unduh **KasirWarungPintar-APK**.
6. File yang diunduh berbentuk ZIP → ekstrak → di dalamnya ada
   `kasirwarungpintar-1.0.0-arm64-v8a-debug.apk`.

> Jika build gagal (tanda ✗ merah), klik run-nya → klik job **build-apk** → lihat
> langkah mana yang berwarna merah, lalu foto/screenshot log bagian itu untuk ditanyakan kembali.

---

## 5. Memasang APK di Tablet 8 Inci

1. Salin file `.apk` ke tablet (USB, Google Drive, WhatsApp ke diri sendiri, dsb.).
2. Buka file APK dari file manager tablet.
3. Saat diminta, izinkan **"Install aplikasi tidak dikenal / Install unknown apps"**
   untuk aplikasi file manager tersebut (pengaturan keamanan, sekali saja).
4. Klik **Install** → selesai. Ikon **Kasir Warung Pintar** muncul di layar utama.
5. Login pertama: **pemilik / owner123** atau **kasir / kasir123** (segera ganti di Pengaturan).

> APK ini arsitektur **arm64-v8a** — kompatibel dengan hampir semua tablet modern
> (2018 ke atas), termasuk tablet 8 inci.
> Data tersimpan di penyimpanan internal aplikasi (aman, tidak butuh izin apa pun).

---

## 6. Ringkasan Alur

```
Unzip paket terbaru → tampilkan folder tersembunyi
        ↓
Upload SEMUA isi folder ke repo GitHub (Cara A atau B)
        ↓
GitHub → tab Actions → Build APK Android → Run workflow
        ↓
Tunggu ± 20–40 menit → unduh artifact KasirWarungPintar-APK
        ↓
Ekstrak ZIP → salin .apk ke tablet → Install
```
