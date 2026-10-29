# Dokumentasi Pengujian SkillBridge API

## 1. Informasi Proyek

- **Nama Proyek:** SkillBridge API
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Tools Pengujian:** Swagger UI, PostgreSQL, dan Pytest
- **Bahasa Pemrograman:** Python

## 2. Tujuan Pengujian

Pengujian dilakukan untuk memastikan endpoint API SkillBridge berjalan sesuai fungsinya, termasuk autentikasi, pembatasan akses pengguna, pendaftaran kursus, pembayaran, callback pembayaran, dan progres pembelajaran.

## 3. Hasil Pengujian Manual

| No. | Skenario Pengujian | Hasil Aktual | Status |
|---|---|---|---|
| 1 | Melihat katalog kursus | HTTP 200, data kursus ditampilkan | Berhasil |
| 2 | Melihat detail kursus | HTTP 200, detail kursus dan modul ditampilkan | Berhasil |
| 3 | Registrasi pengguna | HTTP 201, akun berhasil dibuat | Berhasil |
| 4 | Login pengguna | HTTP 200, access token diperoleh | Berhasil |
| 5 | Melihat profil pengguna | HTTP 200, data pengguna ditampilkan | Berhasil |
| 6 | Student membuat kursus | HTTP 403, akses ditolak | Berhasil |
| 7 | Mendaftar kursus | HTTP 201, enrollment dan tagihan dibuat | Berhasil |
| 8 | Mendaftar kursus yang sama dua kali | HTTP 409, pendaftaran duplikat ditolak | Berhasil |
| 9 | Mendaftar dengan email duplikat | HTTP 409, email ditolak | Berhasil |
| 10 | Registrasi dengan password terlalu pendek | HTTP 422, validasi gagal | Berhasil |
| 11 | Mengakses kursus menggunakan ID bukan UUID | HTTP 422, validasi gagal | Berhasil |
| 12 | Membuat pembayaran | HTTP 201, pembayaran berstatus pending | Berhasil |
| 13 | Callback tanpa token rahasia | HTTP 401, callback ditolak | Berhasil |
| 14 | Callback dengan nominal salah | HTTP 422, nominal ditolak | Berhasil |
| 15 | Callback pembayaran berhasil | HTTP 200, pembayaran diproses | Berhasil |
| 16 | Callback pembayaran duplikat | HTTP 200, callback tidak diproses ulang | Berhasil |
| 17 | Memperbarui progres modul | HTTP 200, progres menjadi 25% | Berhasil |

## 4. Verifikasi Database

Pemeriksaan melalui PostgreSQL menunjukkan bahwa kedua transaksi yang diuji memiliki status order, invoice, dan payment `paid`, serta enrollment `active`.

Pemeriksaan kolom `password_hash` pada akun pengujian menunjukkan bahwa nilai yang tersimpan berbeda dari password aslinya, sehingga password tidak disimpan sebagai teks biasa.

Pengujian progres juga menunjukkan bahwa satu dari empat modul yang diselesaikan menghasilkan persentase progres sebesar 25%.

## 5. Hasil Pengujian Otomatis

Pengujian otomatis dilakukan menggunakan perintah:

`python -m pytest -v`

Hasil pengujian:

- Jumlah tes: 7
- Tes berhasil: 7
- Tes gagal: 0
- Waktu pengujian: 3,79 detik

Seluruh tujuh tes otomatis yang dijalankan berstatus `PASSED`.

## 6. Kesimpulan

Berdasarkan pengujian manual yang telah dilakukan dan tujuh pengujian otomatis yang berhasil, fungsi utama SkillBridge API yang diuji berjalan sesuai dengan hasil yang diharapkan. Pengujian mencakup autentikasi, validasi input, pembatasan akses, enrollment, pembayaran, callback, dan progres pembelajaran.

Pengujian menggunakan koleksi Insomnia dan pemeriksaan seluruh endpoint tetap perlu dikonfirmasi untuk memastikan semua kebutuhan pengujian proyek telah terpenuhi.
