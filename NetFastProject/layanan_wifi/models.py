# GANTI SEMUA ISI models.py DENGAN INI:

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Model-model ini dibuat berdasarkan file layanan_wifi.sql Anda
# 'managed = False' berarti Django tidak akan mengubah tabel ini saat migrasi

class AreaLayanan(models.Model):
    id_area_layanan = models.AutoField(primary_key=True)
    nama_area = models.CharField(unique=True, max_length=100)
    kode_pos = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_layanan'

    def __str__(self):
        return self.nama_area

class JenisJasa(models.Model):
    id_jenis_jasa = models.AutoField(primary_key=True)
    nama_jasa = models.CharField(unique=True, max_length=100)
    biaya = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jenis_jasa'

    def __str__(self):
        return self.nama_jasa

class JenisPerangkat(models.Model):
    id_jenis_perangkat = models.AutoField(primary_key=True)
    nama_jenis = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'jenis_perangkat'

    def __str__(self):
        return self.nama_jenis

class MetodePembayaran(models.Model):
    id_metode_bayar = models.AutoField(primary_key=True)
    nama_metode = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'metode_pembayaran'

    def __str__(self):
        return self.nama_metode

class PaketLayanan(models.Model):
    id_paket = models.AutoField(primary_key=True)
    nama_paket = models.CharField(unique=True, max_length=100)
    kecepatan_mbps = models.IntegerField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paket_layanan'

    def __str__(self):
        return self.nama_paket

class Pelanggan(models.Model):
    id_pelanggan = models.AutoField(primary_key=True)
    nama_lengkap = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    alamat_pemasangan = models.TextField()
    no_telepon = models.CharField(max_length=15, blank=True, null=True)
    tanggal_daftar = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'pelanggan'

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.nama_lengkap

class Teknisi(models.Model):
    id_teknisi = models.AutoField(primary_key=True)
    nama_teknisi = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    role_akses = models.CharField(max_length=7)
    no_telepon = models.CharField(max_length=15, blank=True, null=True)
    id_area_layanan = models.ForeignKey(AreaLayanan, models.DO_NOTHING, db_column='id_area_layanan', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teknisi'

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)
    
    def __str__(self):
        return self.nama_teknisi

class Langganan(models.Model):
    id_langganan = models.AutoField(primary_key=True)
    id_pelanggan = models.ForeignKey(Pelanggan, models.DO_NOTHING, db_column='id_pelanggan', null=True, blank=True)
    id_paket = models.ForeignKey(PaketLayanan, models.DO_NOTHING, db_column='id_paket', null=True, blank=True)
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField(blank=True, null=True)
    status_langganan = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'langganan'

class Pembayaran(models.Model):
    id_pembayaran = models.AutoField(primary_key=True)
    id_langganan = models.ForeignKey(Langganan, models.DO_NOTHING, db_column='id_langganan')
    id_metode_bayar = models.ForeignKey(MetodePembayaran, models.DO_NOTHING, db_column='id_metode_bayar')
    jumlah_bayar = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal_bayar = models.DateTimeField()
    periode_tagihan = models.DateField(blank=True, null=True)
    status_pembayaran = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'pembayaran'

class PemesananJasa(models.Model):
    id_pemesanan = models.AutoField(primary_key=True)
    id_pelanggan = models.ForeignKey(Pelanggan, models.DO_NOTHING, db_column='id_pelanggan')
    id_jenis_jasa = models.ForeignKey(JenisJasa, models.DO_NOTHING, db_column='id_jenis_jasa')
    id_teknisi = models.ForeignKey(Teknisi, models.DO_NOTHING, db_column='id_teknisi', blank=True, null=True)
    tanggal_pemesanan = models.DateTimeField(auto_now_add=True)
    tanggal_jadwal = models.DateField(blank=True, null=True)
    status_pemesanan = models.CharField(max_length=18)
    catatan = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pemesanan_jasa'

class Perangkat(models.Model):
    id_perangkat = models.AutoField(primary_key=True)
    id_jenis_perangkat = models.ForeignKey(JenisPerangkat, models.DO_NOTHING, db_column='id_jenis_perangkat')
    serial_number = models.CharField(unique=True, max_length=100)
    merk_model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perangkat'

class PenempatanPerangkat(models.Model):
    id_penempatan = models.AutoField(primary_key=True)
    id_langganan = models.ForeignKey(Langganan, models.DO_NOTHING, db_column='id_langganan')
    id_perangkat = models.ForeignKey(Perangkat, models.DO_NOTHING, db_column='id_perangkat')
    tanggal_pasang = models.DateField(blank=True, null=True)
    status_perangkat = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'penempatan_perangkat'
        unique_together = (('id_perangkat', 'id_langganan'),)

class RiwayatTestingWifi(models.Model):
    id_testing = models.AutoField(primary_key=True)
    id_langganan = models.ForeignKey(Langganan, models.DO_NOTHING, db_column='id_langganan', null=True, blank=True)
    waktu_testing = models.DateTimeField(auto_now_add=True)
    download_speed_mbps = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    upload_speed_mbps = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ping_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'riwayat_testing_wifi'

# Model dari .sql Anda tidak memiliki tabel LaporanTeknisi, Tagihan, atau Notifikasi.
# Model-model tersebut dari kode lama Anda (models.py) tidak akan saya masukkan
# karena tidak ada tabelnya di layanan_wifi.sql.
