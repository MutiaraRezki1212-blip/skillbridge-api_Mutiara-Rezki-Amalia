# Dokumentasi Pengujian SkillBridge API

## 1. Informasi Proyek

- **Nama Proyek:** SkillBridge API
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Tools Pengujian:** Swagger UI, PostgreSQL, dan Pytest
- **Bahasa Pemrograman:** Python

## 2. Tujuan Pengujian

Pengujian dilakukan untuk memastikan endpoint API SkillBridge berjalan sesuai fungsinya, termasuk autentikasi, pembatasan akses pengguna, pendaftaran kursus, pembayaran, callback pembayaran, dan progres pembelajaran.

Pengujian juga mencakup validasi signature callback menggunakan HMAC-SHA256 serta pemeriksaan masa berlaku invoice.

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
| 13 | Callback tanpa signature | HTTP 401, callback ditolak | Berhasil |
| 14 | Callback dengan signature tidak valid | HTTP 401, callback ditolak | Berhasil |
| 15 | Callback dengan nominal salah | HTTP 422, nominal ditolak | Berhasil |
| 16 | Callback pembayaran berhasil | HTTP 200, pembayaran diproses | Berhasil |
| 17 | Callback pembayaran duplikat | HTTP 200, callback tidak diproses ulang | Berhasil |
| 18 | Memperbarui progres modul | HTTP 200, progres menjadi 25% | Berhasil |

*Catatan: tabel ini merangkum hasil pengujian yang telah dilakukan. Skenario signature yang salah juga diperiksa melalui pengujian otomatis.*

## 4. Verifikasi Database

Pemeriksaan melalui PostgreSQL menunjukkan bahwa transaksi yang diuji memiliki status order, invoice, dan payment `paid`, serta enrollment `active`.

Pemeriksaan kolom `password_hash` pada akun pengujian menunjukkan bahwa nilai yang tersimpan berbeda dari password aslinya, sehingga password tidak disimpan sebagai teks biasa.

Pengujian progres juga menunjukkan bahwa penyelesaian satu dari empat modul menghasilkan persentase progres sebesar 25%.

## 5. Hasil Pengujian Otomatis

Pengujian otomatis dilakukan menggunakan perintah:

```bash
python -m pytest -v
```

Hasil pengujian terakhir:

- **Jumlah tes:** 8
- **Tes berhasil:** 8
- **Tes gagal:** 0
- **Tes error:** 0
- **Waktu pengujian:** 4,13 detik

Seluruh delapan tes otomatis berstatus `PASSED`.

Pengujian otomatis mencakup:

1. Registrasi pengguna dan penolakan data duplikat.
2. Validasi input.
3. Kesalahan autentikasi.
4. Pembatasan hak akses berdasarkan peran.
5. Validasi pencarian kursus.
6. Alur pembelian dan pembayaran.
7. Pembayaran gagal dan percobaan ulang.
8. Penolakan callback pembayaran ketika invoice sudah kedaluwarsa.

Pengujian callback juga menggunakan signature HMAC-SHA256 yang dihitung dari raw body permintaan. Signature yang tidak valid ditolak dengan HTTP 401, sedangkan nominal pembayaran yang tidak sesuai ditolak dengan HTTP 422.

Pengujian invoice kedaluwarsa memastikan callback pembayaran ditolak dengan HTTP 409.

## 6. Kesimpulan

Berdasarkan hasil pengujian manual dan delapan pengujian otomatis yang berhasil, fungsi utama SkillBridge API yang telah diuji berjalan sesuai dengan hasil yang diharapkan.

Pengujian mencakup autentikasi, validasi input, pembatasan akses, enrollment, pembayaran, verifikasi signature callback, pemeriksaan kedaluwarsa invoice, dan progres pembelajaran.

Pengujian menggunakan koleksi Insomnia dan pemeriksaan seluruh endpoint masih perlu diselesaikan atau dikonfirmasi untuk memastikan seluruh kebutuhan pengujian proyek telah terpenuhi.
