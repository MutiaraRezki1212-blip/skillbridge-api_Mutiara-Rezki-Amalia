# Dokumentasi Pengujian SkillBridge API

## 1. Informasi Proyek

- **Nama Proyek:** SkillBridge API
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Tools Pengujian:** Insomnia, Swagger UI, PostgreSQL, dan Pytest
- **Bahasa Pemrograman:** Python

## 2. Tujuan Pengujian

Pengujian dilakukan untuk memastikan endpoint API SkillBridge berjalan sesuai fungsinya, termasuk autentikasi, pembatasan akses pengguna, pendaftaran kursus, pembayaran, callback pembayaran, dan progres pembelajaran.

Pengujian juga mencakup validasi signature callback menggunakan HMAC-SHA256, pemeriksaan masa berlaku invoice, serta pembatasan akses berdasarkan peran dan kepemilikan data.

Selain pengujian fitur utama, dilakukan pengembangan dan pengujian beberapa endpoint tambahan sebagai bagian dari Latihan Mandiri.

## 3. Hasil Pengujian Manual

Pengujian manual dilakukan menggunakan Swagger UI dan Insomnia. Pengujian awal menggunakan Swagger UI, sedangkan pengujian lanjutan dan dokumentasi hasil pengujian dilakukan menggunakan Insomnia.

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

*Catatan: tabel ini merangkum pengujian fitur utama yang telah dilakukan. Skenario signature yang salah juga diperiksa melalui pengujian otomatis.*

## 4. Hasil Pengujian Latihan Mandiri

Pengujian Latihan Mandiri dilakukan untuk memeriksa endpoint tambahan dan memastikan sistem menerapkan aturan pengambilan data, kepemilikan, serta hak akses pengguna sesuai perannya.

### 4.1 Latihan Mandiri 1 – Mengambil Daftar Modul Kursus

**Endpoint:** `GET /courses/{course_id}/modules`

Pengujian dilakukan untuk mengambil daftar modul berdasarkan ID kursus tertentu.

**Hasil pengujian:**
- Status HTTP: **200 OK**
- Sistem berhasil menampilkan empat modul kursus.
- Modul ditampilkan berdasarkan urutan posisi dari 1 sampai 4.

Modul yang berhasil ditampilkan:
1. Pengenalan REST
2. Routing dan Validasi
3. Database dan ORM
4. Autentikasi JWT

**Kesimpulan:**

Endpoint berhasil mengambil seluruh modul dari kursus yang dipilih. Data modul ditampilkan beserta ID, judul, dan posisi masing-masing. Urutan modul sudah sesuai dengan nilai `position`, sehingga endpoint berhasil menjalankan fungsi pengambilan daftar modul kursus secara berurutan.

### 4.2 Latihan Mandiri 2 – Mengambil Detail Pembayaran Berdasarkan Kepemilikan

**Endpoint:** `GET /payments/{payment_id}`

Pengujian dilakukan untuk memastikan mahasiswa hanya dapat melihat pembayaran miliknya sendiri.

**Hasil pengujian:**

| Skenario | Hasil Aktual | Status |
|---|---|---|
| Mahasiswa pemilik pembayaran mengakses detail pembayaran | HTTP 200, data pembayaran ditampilkan | Berhasil |
| Mahasiswa lain mencoba mengakses pembayaran tersebut | HTTP 404, pembayaran tidak ditemukan | Berhasil |

**Kesimpulan:**

Endpoint berhasil menerapkan pemeriksaan kepemilikan pembayaran. Mahasiswa yang memiliki pembayaran dapat melihat detail pembayaran menggunakan token autentikasinya sendiri. Sebaliknya, mahasiswa lain tidak dapat mengakses pembayaran tersebut karena sistem menolak permintaan dengan HTTP 404.

### 4.3 Latihan Mandiri 3 – Memperbarui Kursus Berdasarkan Role dan Kepemilikan

**Endpoint:** `PATCH /courses/{course_id}`

Pengujian dilakukan untuk memastikan Instructor hanya dapat memperbarui kursus miliknya sendiri, sedangkan Admin memiliki wewenang untuk memperbarui kursus milik pengguna lain.

**Hasil pengujian:**

| Skenario | Hasil Aktual | Status |
|---|---|---|
| Instructor memperbarui kursus miliknya sendiri | HTTP 200, data kursus berhasil diperbarui | Berhasil |
| Instructor memperbarui kursus milik Admin | HTTP 403, akses ditolak | Berhasil |
| Admin memperbarui kursus milik pengguna lain | HTTP 200, data kursus berhasil diperbarui | Berhasil |

**Kesimpulan:**

Endpoint berhasil menerapkan pembatasan hak akses berdasarkan peran dan kepemilikan kursus. Instructor hanya dapat mengubah kursus miliknya sendiri, sedangkan Admin memiliki wewenang untuk mengubah kursus milik pengguna lain.

### 4.4 Latihan Mandiri 4 – Pemeriksaan Kedaluwarsa Invoice pada Callback Pembayaran

**Endpoint:** `POST /payments/callback`

Pengujian dilakukan untuk memastikan sistem menolak callback pembayaran berhasil apabila invoice sudah melewati masa berlakunya.

Invoice dibuat dengan masa berlaku 24 jam setelah diterbitkan. Ketika callback pembayaran diterima, sistem memeriksa waktu kedaluwarsa invoice sebelum mengubah status pembayaran menjadi berhasil.

**Hasil pengujian:**
- Status HTTP: **409 Conflict**
- Pesan respons: `Invoice sudah kedaluwarsa`
- Callback pembayaran ditolak karena invoice telah melewati masa berlaku.

**Kesimpulan:**

Endpoint callback berhasil memeriksa masa berlaku invoice sebelum memproses pembayaran. Apabila invoice sudah kedaluwarsa, sistem menolak callback dengan HTTP 409 sehingga pembayaran tidak diproses sebagai pembayaran berhasil.

## 5. Verifikasi Database

Pemeriksaan melalui PostgreSQL menunjukkan bahwa transaksi yang diuji memiliki status order, invoice, dan payment `paid`, serta enrollment `active`.

Pemeriksaan kolom `password_hash` pada akun pengujian menunjukkan bahwa nilai yang tersimpan berbeda dari password aslinya, sehingga password tidak disimpan sebagai teks biasa.

Pengujian progres juga menunjukkan bahwa penyelesaian satu dari empat modul menghasilkan persentase progres sebesar 25%.

## 6. Hasil Pengujian Otomatis

Pengujian otomatis dilakukan menggunakan perintah:

```bash
python -m pytest -v
```

Hasil pengujian terakhir:

- **Jumlah tes:** 10
- **Tes berhasil:** 10
- **Tes gagal:** 0
- **Tes error:** 0
- **Waktu pengujian:** 6,68 detik

Seluruh sepuluh tes otomatis berstatus `PASSED`.

Pengujian otomatis mencakup:

1. Registrasi pengguna dan penolakan data duplikat.
2. Validasi input.
3. Kesalahan autentikasi.
4. Pembatasan hak akses berdasarkan peran.
5. Validasi pencarian kursus.
6. Pengambilan daftar modul kursus berdasarkan urutan.
7. Pembaruan kursus berdasarkan role dan kepemilikan.
8. Alur pembelian dan pembayaran.
9. Pembayaran gagal dan percobaan ulang.
10. Penolakan callback pembayaran ketika invoice sudah kedaluwarsa.

Pengujian callback juga menggunakan signature HMAC-SHA256 yang dihitung dari raw body permintaan. Signature yang tidak valid ditolak dengan HTTP 401, sedangkan nominal pembayaran yang tidak sesuai ditolak dengan HTTP 422.

Pengujian invoice kedaluwarsa memastikan callback pembayaran ditolak dengan HTTP 409.

## 7. Kesimpulan

Berdasarkan hasil pengujian manual dan sepuluh pengujian otomatis yang berhasil, fungsi utama SkillBridge API yang telah diuji berjalan sesuai dengan hasil yang diharapkan.

Pengujian mencakup autentikasi, validasi input, pembatasan akses, enrollment, pembayaran, verifikasi signature callback, pemeriksaan kedaluwarsa invoice, progres pembelajaran, pengambilan daftar modul, serta pembaruan kursus berdasarkan role dan kepemilikan.

Hasil pengujian Latihan Mandiri juga menunjukkan bahwa endpoint tambahan telah menjalankan fungsi sesuai kebutuhan. Sistem mampu mengatur akses pengguna berdasarkan kepemilikan data dan peran, serta menolak callback pembayaran ketika invoice sudah kedaluwarsa.

Dengan demikian, pengujian yang telah dilakukan menunjukkan bahwa fitur-fitur SkillBridge API yang diuji dapat berjalan sesuai skenario yang ditetapkan. 
