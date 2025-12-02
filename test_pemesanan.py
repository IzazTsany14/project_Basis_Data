#!/usr/bin/env python
import os, sys, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE','NetFastProject.settings')
sys.path.insert(0,r'c:\project_Basis_Data\NetFastProject')
django.setup()
from django.test import Client
from layanan_wifi.models import Pelanggan, PemesananJasa, JenisJasa
from django.contrib.sessions.backends.db import SessionStore

print('TEST PEMESANAN')
pel = Pelanggan.objects.first()
if not pel:
    print('No pelanggan found')
    sys.exit(1)
print('Pelanggan', pel.id_pelanggan)

client = Client()
s = SessionStore()
s['pelanggan_id'] = pel.id_pelanggan
s.save()
client.cookies['sessionid'] = s.session_key

# Ensure JenisJasa exists
jenis = JenisJasa.objects.first()
if not jenis:
    from layanan_wifi.models import JenisJasa as JJ
    jenis = JJ.objects.create(nama_jasa='Instalasi', biaya=0)

payload = {'id_jenis_jasa': jenis.id_jenis_jasa, 'catatan': 'Test via script'}
resp = client.post('/user/pemesanan/', data=json.dumps(payload), content_type='application/json', HTTP_X_CSRFTOKEN='dummy')
print('Status', resp.status_code)
print('Body', resp.content.decode())
if resp.status_code==201:
    print('Created OK')
    last = PemesananJasa.objects.filter(id_pelanggan=pel).order_by('-tanggal_pemesanan').first()
    print('Last pemesanan id', last.id_pemesanan)
else:
    print('Failed')
