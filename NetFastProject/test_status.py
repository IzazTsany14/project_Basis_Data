#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetFastProject.settings')
django.setup()

from layanan_wifi.models import Pelanggan, Langganan

# Check first 3 pelanggan
for p in Pelanggan.objects.all()[:3]:
    print(f"\nPelanggan: {p.nama_lengkap} (ID: {p.id_pelanggan})")
    lang = Langganan.objects.filter(id_pelanggan=p).order_by('-tanggal_mulai').first()
    if lang:
        print(f"  Langganan ID: {lang.id_langganan}")
        print(f"  Status (raw): '{lang.status_langganan}'")
        print(f"  Status (type): {type(lang.status_langganan)}")
        if lang.status_langganan:
            print(f"  Status (upper): '{lang.status_langganan.strip().upper()}'")
    else:
        print(f"  No langganan")
