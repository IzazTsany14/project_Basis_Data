#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetFastProject.settings')
django.setup()

from layanan_wifi.models import Langganan, Pelanggan, AreaLayanan

# Simulate API response for first 3 pelanggan
pelanggan_qs = Pelanggan.objects.all().order_by('-tanggal_daftar')[:3]
areas = list(AreaLayanan.objects.all())

for p in pelanggan_qs:
    print(f"\n=== Pelanggan: {p.nama_lengkap} (ID: {p.id_pelanggan})")
    
    # Find latest langganan
    lang = Langganan.objects.filter(id_pelanggan=p).order_by('-tanggal_mulai').first()
    
    if lang:
        print(f"  Langganan ID: {lang.id_langganan}")
        print(f"  Raw status_langganan: '{lang.status_langganan}'")
        print(f"  Type: {type(lang.status_langganan)}")
        status_langganan = lang.status_langganan
        if status_langganan:
            status_langganan = status_langganan.strip().upper()
        print(f"  Processed status: '{status_langganan}'")
        print(f"  can_suspend: {status_langganan == 'AKTIF'}")
        print(f"  can_resume: {status_langganan == 'SUSPEND'}")
    else:
        print("  No langganan found")
