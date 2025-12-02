#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetFastProject.settings')
django.setup()

from layanan_wifi.models import Langganan, Pelanggan

# Check langganan data
langganan_list = Langganan.objects.all()
print("=== Total Langganan:", langganan_list.count())
for lang in langganan_list[:5]:
    print(f"ID: {lang.id_langganan}, Pelanggan: {lang.id_pelanggan.nama_lengkap if lang.id_pelanggan else 'None'}, Status: '{lang.status_langganan}', Paket: {lang.id_paket.nama_paket if lang.id_paket else 'None'}")

print("\n=== Pelanggan dengan langganan:")
for p in Pelanggan.objects.all()[:5]:
    lang = Langganan.objects.filter(id_pelanggan=p).order_by('-tanggal_mulai').first()
    if lang:
        print(f"Pelanggan: {p.nama_lengkap}, Status: '{lang.status_langganan.strip() if lang.status_langganan else 'None'}'")
    else:
        print(f"Pelanggan: {p.nama_lengkap}, Status: No langganan")
