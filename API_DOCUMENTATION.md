# NetFast API Documentation

Backend API untuk sistem layanan WiFi NetFast menggunakan Django dan MySQL.

## Struktur Proyek

```
NetFastProject/
├── manage.py
├── NetFastProject/
│   ├── settings.py          # Konfigurasi MySQL dan Apps
│   └── urls.py              # Routing Global
└── layanan_wifi/
    ├── models.py            # 13 Model Database (ORM)
    ├── serializers.py       # Konversi Model ke JSON
    ├── views.py             # Logika Bisnis & CRUD
    ├── urls.py              # Routing Lokal API
    └── admin.py             # Panel Admin Django
```

## Setup Database MySQL

### 1. Konfigurasi Environment

Salin file `.env.example` menjadi `.env` dan sesuaikan:

```bash
DB_NAME=netfast_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 2. Instalasi Dependencies

```bash
pip install -r requirements.txt
```

### 3. Migrasi Database

```bash
cd NetFastProject
python manage.py makemigrations
python manage.py migrate
```

### 4. Membuat Superuser (Opsional untuk Admin Panel)

```bash
python manage.py createsuperuser
```

### 5. Menjalankan Server

```bash
python manage.py runserver
```

Server akan berjalan di `http://localhost:8000`

## 13 Model Database

1. **Pelanggan** - Data pelanggan
2. **Teknisi** - Data teknisi
3. **Admin** - Data admin sistem
4. **PaketLayanan** - Paket layanan WiFi
5. **Langganan** - Langganan pelanggan
6. **PemesananJasa** - Pemesanan jasa (Instalasi, Perbaikan, dll)
7. **LaporanTeknisi** - Laporan kerja teknisi
8. **Pembayaran** - Data pembayaran
9. **Tagihan** - Data tagihan bulanan
10. **Perangkat** - Perangkat yang dipasang
11. **RiwayatTestingWifi** - Hasil speed test
12. **Notifikasi** - Notifikasi ke pelanggan
13. **Admin** - Data administrator

## API Endpoints

### Autentikasi

#### Login (3 Role: Pelanggan, Teknisi, Admin)
```
POST /api/auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "pelanggan"
}
```

**Response (Success):**
```json
{
  "message": "Login berhasil",
  "user": {
    "id_pelanggan": 1,
    "nama_pelanggan": "John Doe",
    "email": "user@example.com",
    "role": "pelanggan"
  }
}
```

#### Registrasi Pelanggan Baru
```
POST /api/auth/registrasi/
```

**Request Body:**
```json
{
  "nama_pelanggan": "John Doe",
  "email": "john@example.com",
  "no_telepon": "081234567890",
  "alamat": "Jl. Contoh No. 123",
  "password": "password123"
}
```

---

### Endpoint Pelanggan (User)

#### Melihat Riwayat Pemesanan
```
GET /api/user/pemesanan/?id_pelanggan=1
```

#### Membuat Pemesanan Jasa Baru
```
POST /api/user/pemesanan/
```

**Request Body:**
```json
{
  "id_pelanggan": 1,
  "jenis_jasa": "Instalasi",
  "tanggal_pelaksanaan": "2025-11-01",
  "catatan": "Instalasi baru",
  "biaya_jasa": 500000.00
}
```

**Response (Success):**
```json
{
  "message": "Pemesanan berhasil dibuat",
  "pemesanan": {
    "id_pemesanan": 5,
    "status_pemesanan": "Menunggu Penugasan",
    "jenis_jasa": "Instalasi"
  }
}
```

#### Melihat Langganan Aktif
```
GET /api/user/langganan/?id_pelanggan=1
```

#### Melihat Notifikasi
```
GET /api/user/notifikasi/?id_pelanggan=1
```

#### Tandai Notifikasi Sudah Dibaca
```
PUT /api/user/notifikasi/{id_notifikasi}/baca/
```

#### Melihat Tagihan
```
GET /api/user/tagihan/?id_pelanggan=1
```

#### Melihat Riwayat Speed Test
```
GET /api/user/riwayat-testing/?id_pelanggan=1
```

---

### Speed Test

#### Menyimpan Hasil Speed Test
```
POST /api/testing/save/
```

**Request Body:**
```json
{
  "id_pelanggan": 1,
  "kecepatan_download": 95.5,
  "kecepatan_upload": 45.2,
  "ping": 15,
  "lokasi_testing": "Ruang Tamu",
  "status_hasil": "Sesuai"
}
```

**Logika:**
- Sistem akan otomatis mencari langganan aktif berdasarkan `id_pelanggan`
- Data disimpan ke tabel `RIWAYAT_TESTING_WIFI` dengan FK ke `LANGGANAN`
- Notifikasi otomatis dibuat untuk pelanggan

**Response (Success):**
```json
{
  "message": "Data speed test berhasil disimpan",
  "testing": {
    "id_testing": 10,
    "kecepatan_download": "95.50",
    "kecepatan_upload": "45.20",
    "ping": 15
  }
}
```

---

### Endpoint Teknisi

#### Melihat Tugas yang Ditugaskan
```
GET /api/teknisi/tugas/?id_teknisi=1
```

**Response:**
```json
[
  {
    "id_pemesanan": 5,
    "nama_pelanggan": "John Doe",
    "jenis_jasa": "Instalasi",
    "status_pemesanan": "Ditugaskan",
    "tanggal_pelaksanaan": "2025-11-01"
  }
]
```

#### Update Status Pemesanan
```
PUT /api/teknisi/pemesanan/{id_pemesanan}/update/
```

**Request Body:**
```json
{
  "status_pemesanan": "Dalam Proses"
}
```

#### Membuat Laporan Teknisi
```
POST /api/teknisi/laporan/
```

**Request Body:**
```json
{
  "id_pemesanan": 5,
  "id_teknisi": 1,
  "deskripsi_pekerjaan": "Instalasi router dan modem selesai",
  "status_pekerjaan": "Berhasil",
  "catatan_tambahan": "Semua berjalan lancar"
}
```

**Logika:**
- Jika `status_pekerjaan` = "Berhasil", maka `status_pemesanan` otomatis berubah menjadi "Selesai"
- Notifikasi otomatis dikirim ke pelanggan

---

### Endpoint Admin

#### Melihat Pemesanan yang Menunggu Penugasan
```
GET /api/admin/pemesanan/menunggu/
```

**Response:**
```json
[
  {
    "id_pemesanan": 5,
    "nama_pelanggan": "John Doe",
    "jenis_jasa": "Instalasi",
    "status_pemesanan": "Menunggu Penugasan",
    "tanggal_pemesanan": "2025-10-28T10:30:00Z"
  }
]
```

#### Menugaskan Teknisi ke Pemesanan
```
POST /api/admin/penugasan/
```

**Request Body:**
```json
{
  "id_pemesanan": 5,
  "id_teknisi": 1
}
```

**Logika:**
1. Validasi teknisi harus berstatus "Tersedia"
2. Update kolom `id_teknisi` di tabel `PEMESANAN_JASA`
3. Update `status_pemesanan` menjadi "Ditugaskan"
4. Notifikasi otomatis dikirim ke pelanggan

**Response (Success):**
```json
{
  "message": "Teknisi berhasil ditugaskan",
  "pemesanan": {
    "id_pemesanan": 5,
    "nama_teknisi": "Ahmad Rizki",
    "status_pemesanan": "Ditugaskan"
  }
}
```

#### Melihat Teknisi yang Tersedia
```
GET /api/admin/teknisi/tersedia/
```

#### CRUD Paket Layanan

**List Semua Paket:**
```
GET /api/admin/paket/
```

**Detail Paket:**
```
GET /api/admin/paket/{id_paket}/
```

**Buat Paket Baru:**
```
POST /api/admin/paket/
```

**Request Body:**
```json
{
  "nama_paket": "Paket Premium",
  "kecepatan_download": 100,
  "kecepatan_upload": 50,
  "harga_bulanan": 500000.00,
  "kuota_data": "Unlimited",
  "deskripsi": "Paket internet super cepat"
}
```

**Update Paket:**
```
PUT /api/admin/paket/{id_paket}/
```

**Hapus Paket:**
```
DELETE /api/admin/paket/{id_paket}/
```

#### Dashboard Statistics
```
GET /api/admin/dashboard/stats/
```

**Response:**
```json
{
  "total_pelanggan": 150,
  "total_teknisi": 10,
  "teknisi_tersedia": 7,
  "pemesanan_menunggu": 5,
  "langganan_aktif": 145
}
```

---

## Panel Admin Django

Akses panel admin Django di `http://localhost:8000/admin/`

Panel admin menyediakan interface untuk CRUD langsung terhadap semua 13 model database.

---

## Workflow 3 Peran

### 1. Pelanggan
- Registrasi akun
- Login
- Buat pemesanan jasa (Instalasi, Perbaikan, Upgrade, Maintenance)
- Jalankan speed test dan simpan hasil
- Lihat riwayat pemesanan
- Lihat tagihan dan notifikasi

### 2. Teknisi
- Login
- Lihat tugas yang ditugaskan
- Update status pemesanan (Dalam Proses, Selesai)
- Buat laporan pekerjaan

### 3. Admin
- Login
- Lihat pemesanan yang menunggu penugasan
- Tugaskan teknisi ke pemesanan
- Lihat teknisi yang tersedia
- CRUD paket layanan
- Lihat statistik dashboard

---

## Relasi Foreign Key Penting

1. `LANGGANAN.id_pelanggan` → `PELANGGAN.id_pelanggan`
2. `LANGGANAN.id_paket` → `PAKET_LAYANAN.id_paket`
3. `PEMESANAN_JASA.id_pelanggan` → `PELANGGAN.id_pelanggan`
4. `PEMESANAN_JASA.id_teknisi` → `TEKNISI.id_teknisi`
5. `RIWAYAT_TESTING_WIFI.id_langganan` → `LANGGANAN.id_langganan`

---

## Demonstrasi Fitur Utama

### Demo 1: Penugasan Teknisi
1. Pelanggan membuat pemesanan (status: "Menunggu Penugasan")
2. Admin melihat pemesanan yang menunggu
3. Admin tugaskan teknisi (status berubah: "Ditugaskan")
4. Kolom `id_teknisi` di database terisi

### Demo 2: Speed Test
1. Pelanggan login dan memiliki langganan aktif
2. Pelanggan jalankan speed test
3. Data disimpan ke `RIWAYAT_TESTING_WIFI` dengan FK ke `LANGGANAN` yang aktif
4. Notifikasi otomatis dibuat

---

## Testing dengan Postman/cURL

**Contoh cURL untuk Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@netfast.com",
  "password": "admin123",
  "role": "admin"
}'
```

**Contoh cURL untuk Penugasan Teknisi:**
```bash
curl -X POST http://localhost:8000/api/admin/penugasan/ \
-H "Content-Type: application/json" \
-d '{
  "id_pemesanan": 5,
  "id_teknisi": 1
}'
```

**Contoh cURL untuk Save Speed Test:**
```bash
curl -X POST http://localhost:8000/api/testing/save/ \
-H "Content-Type: application/json" \
-d '{
  "id_pelanggan": 1,
  "kecepatan_download": 95.5,
  "kecepatan_upload": 45.2,
  "ping": 15,
  "lokasi_testing": "Ruang Tamu",
  "status_hasil": "Sesuai"
}'
```

---

## Catatan Penting

1. **Password Hash**: Semua password di-hash menggunakan Django's `make_password()` dan `check_password()`
2. **Auto Timestamp**: `tanggal_pemesanan`, `tanggal_registrasi`, `tanggal_testing` otomatis terisi
3. **Validasi**: Serializer melakukan validasi data sebelum disimpan ke database
4. **Notifikasi Otomatis**: Sistem otomatis membuat notifikasi saat ada event penting
5. **Status Management**: Status pemesanan otomatis berubah sesuai workflow

---

## Error Handling

Semua endpoint mengembalikan status HTTP yang sesuai:
- `200 OK` - Sukses
- `201 CREATED` - Data berhasil dibuat
- `400 BAD REQUEST` - Data tidak valid
- `401 UNAUTHORIZED` - Login gagal
- `404 NOT FOUND` - Data tidak ditemukan
- `500 INTERNAL SERVER ERROR` - Error server

---

## Pengembangan Selanjutnya

1. Implementasi JWT Token untuk autentikasi
2. Pagination untuk list endpoint
3. Filter dan search untuk query kompleks
4. Upload bukti pembayaran
5. Real-time notification dengan WebSocket
6. Export laporan ke PDF/Excel
