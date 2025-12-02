#!/usr/bin/env python
"""
Test script untuk speed test API
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetFastProject.settings')
sys.path.insert(0, r'c:\project_Basis_Data\NetFastProject')
django.setup()

from layanan_wifi.models import Pelanggan, Langganan, PaketLayanan, RiwayatTestingWifi
from django.test import Client
from django.contrib.sessions.models import Session
import json

print("=" * 60)
print("TESTING SPEED TEST API")
print("=" * 60)

# 1. Check if there's a pelanggan
pelanggan = Pelanggan.objects.first()
if not pelanggan:
    print("❌ No pelanggan found in database")
    sys.exit(1)

print(f"✓ Found pelanggan: {pelanggan.nama_lengkap} (ID: {pelanggan.id_pelanggan})")

# 2. Check if pelanggan has langganan
langganan = Langganan.objects.filter(id_pelanggan=pelanggan).first()
if not langganan:
    print("⚠️  No langganan found for pelanggan, creating one...")
    paket = PaketLayanan.objects.first()
    if not paket:
        print("❌ No paket layanan found, creating one...")
        paket = PaketLayanan.objects.create(
            nama_paket="Test Package",
            kecepatan_mbps=50,
            harga=100000.00
        )
    from datetime import date
    langganan = Langganan.objects.create(
        id_pelanggan=pelanggan,
        id_paket=paket,
        tanggal_mulai=date.today(),
        status_langganan='AKTIF'
    )
    print(f"✓ Created langganan: {langganan.id_langganan}")
else:
    print(f"✓ Found langganan: {langganan.id_langganan} (Paket: {langganan.id_paket.nama_paket})")

# 3. Test API directly
print("\n" + "=" * 60)
print("TESTING API ENDPOINT")
print("=" * 60)

client = Client()

# Create session manually for testing
from django.contrib.sessions.backends.db import SessionStore
session = SessionStore()
session['pelanggan_id'] = pelanggan.id_pelanggan
session['user_role'] = 'pelanggan'
session.save()

# Get the session cookie and set it properly
client.cookies['sessionid'] = session.session_key

# Test POST to save speed test
test_data = {
    'download_speed_mbps': 45.67,
    'upload_speed_mbps': 12.34,
    'ping_ms': 25
}

print(f"\nPOST /api/speed-test/ dengan data:")
print(json.dumps(test_data, indent=2))

response = client.post(
    '/api/speed-test/',
    data=json.dumps(test_data),
    content_type='application/json',
    HTTP_X_CSRFTOKEN='dummy'
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.content.decode('utf-8')}")

if response.status_code == 201:
    print("\n✓ Speed test saved successfully!")
    
    # Check if data is in database
    latest_test = RiwayatTestingWifi.objects.filter(
        id_langganan=langganan
    ).order_by('-waktu_testing').first()
    
    if latest_test:
        print(f"\n✓ Data found in database:")
        print(f"  - ID: {latest_test.id_testing}")
        print(f"  - Download: {latest_test.download_speed_mbps} Mbps")
        print(f"  - Upload: {latest_test.upload_speed_mbps} Mbps")
        print(f"  - Ping: {latest_test.ping_ms} ms")
        print(f"  - Waktu: {latest_test.waktu_testing}")
    else:
        print("❌ Data not found in database")
else:
    print("\n❌ API request failed")

# Test GET
print("\n" + "=" * 60)
print("GET /api/speed-test/")
print("=" * 60)

response = client.get(
    '/api/speed-test/'
)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content.decode('utf-8'))
    print(f"✓ Retrieved {len(data)} test results")
    if data:
        print(f"  Latest result:")
        latest = data[0]
        print(f"    - Download: {latest.get('download_speed_mbps')} Mbps")
        print(f"    - Upload: {latest.get('upload_speed_mbps')} Mbps")
        print(f"    - Ping: {latest.get('ping_ms')} ms")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
