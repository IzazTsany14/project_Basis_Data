# GANTI SEMUA ISI views.py DENGAN INI:

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, date
import hashlib

from .models import (
    Pelanggan, Teknisi, PaketLayanan, Langganan,
    PemesananJasa, RiwayatTestingWifi
)
from .serializers import (
    PelangganSerializer, PelangganRegistrasiSerializer, TeknisiSerializer,
    PaketLayananSerializer, LanggananSerializer,
    PemesananJasaSerializer, PemesananJasaCreateSerializer,
    RiwayatTestingWifiSerializer,
    RiwayatTestingWifiCreateSerializer, LoginSerializer
)

# --- LOGIKA BARU UNTUK LOGIN ---
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def logout(request):
    # Clear custom session flags and Django auth
    request.session.pop('pelanggan_id', None)
    request.session.pop('teknisi_id', None)
    request.session.pop('user_role', None)
    try:
        auth_logout(request)
    except Exception:
        pass
    
def dashboard_pelanggan_view(request):
    print("Dashboard view called")
    """Session-aware dashboard view for pelanggan.
    The login() view sets request.session['pelanggan_id'] on successful login.
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')

    try:
        pelanggan = Pelanggan.objects.get(id_pelanggan=pelanggan_id)
    except Pelanggan.DoesNotExist:
        return redirect('login')

    langganan = Langganan.objects.filter(id_pelanggan=pelanggan).order_by('-tanggal_mulai').first()
    riwayat_test = RiwayatTestingWifi.objects.filter(id_langganan__id_pelanggan=pelanggan_id).order_by('-waktu_testing')[:5]
    pemesanan_terakhir = PemesananJasa.objects.filter(id_pelanggan=pelanggan).order_by('-tanggal_pemesanan')[:5]

    # Build context matching template variable names
    user_ctx = {
        'nama': getattr(pelanggan, 'nama_lengkap', '') or getattr(pelanggan, 'nama', ''),
        'email': getattr(pelanggan, 'email', ''),
        'no_telp': getattr(pelanggan, 'no_telepon', '') or getattr(pelanggan, 'no_telp', ''),
        'alamat': getattr(pelanggan, 'alamat_pemasangan', '') or getattr(pelanggan, 'alamat', ''),
    }

    paket = None
    if langganan and hasattr(langganan, 'id_paket'):
        paket = langganan.id_paket

    subscription_ctx = {
        'paket_name': getattr(paket, 'nama_paket', '') if paket else 'Belum berlangganan',
        'kecepatan': f"{getattr(paket, 'kecepatan_mbps', '-') } Mbps" if paket else '-',
        'status': 'Aktif' if langganan and getattr(langganan, 'status_langganan', '').lower() == 'aktif' else 'Tidak Aktif'
    }

    recent_services = []
    for s in pemesanan_terakhir:
        jenis = ''
        try:
            jenis = s.id_jenis_jasa.nama_jasa
        except Exception:
            jenis = getattr(s, 'jenis_jasa', '') or ''
        recent_services.append({
            'jenis_jasa': jenis,
            'tanggal_pemesanan': getattr(s, 'tanggal_pemesanan', None),
            'status_pemesanan': getattr(s, 'status_pemesanan', '')
        })

    context = {
        'user': user_ctx,
        'subscription': subscription_ctx,
        'recent_services': recent_services,
    }
    return render(request, 'user/dashboard.html', context)

@api_view(['POST'])
@csrf_exempt
def login(request):
    # Accept either {email,password} or {username,password} or {login_id,password}
    data = request.data if isinstance(request.data, dict) else {}
    password = data.get('password')
    login_id = data.get('login_id') or data.get('email') or data.get('username')

    if not login_id or not password:
        return Response({'error': 'login_id/email/username dan password diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    # Try Pelanggan (by email)
    try:
        pelanggan = Pelanggan.objects.get(email=login_id)
        # Normal Django-hashed password
        if pelanggan.check_password(password):
            request.session['pelanggan_id'] = pelanggan.id_pelanggan
            request.session['user_role'] = 'pelanggan'
            return Response({'message': 'Login berhasil', 'user': {'role': 'pelanggan', 'id': pelanggan.id_pelanggan, 'nama': getattr(pelanggan, 'nama_lengkap', '')}}, status=status.HTTP_200_OK)

        # Legacy fallbacks: plaintext or MD5 stored passwords
        legacy_ok = False
        # plaintext stored in 'password' field
        if hasattr(pelanggan, 'password') and getattr(pelanggan, 'password'):
            if getattr(pelanggan, 'password') == password:
                legacy_ok = True

        # password_hash stored as raw (not Django hash) or MD5
        ph = getattr(pelanggan, 'password_hash', None)
        if not legacy_ok and ph:
            if ph == password:
                legacy_ok = True
            else:
                try:
                    if hashlib.md5(password.encode('utf-8')).hexdigest() == ph:
                        legacy_ok = True
                except Exception:
                    pass

        if legacy_ok:
            # Upgrade to Django hash for future logins
            try:
                pelanggan.set_password(password)
                pelanggan.save()
            except Exception as e:
                print(f"Warning: couldn't upgrade legacy password for pelanggan {getattr(pelanggan,'id_pelanggan',None)}: {e}")
            request.session['pelanggan_id'] = pelanggan.id_pelanggan
            request.session['user_role'] = 'pelanggan'
            return Response({'message': 'Login berhasil (legacy) - password upgraded', 'user': {'role': 'pelanggan', 'id': pelanggan.id_pelanggan, 'nama': getattr(pelanggan, 'nama_lengkap', '')}}, status=status.HTTP_200_OK)
    except Pelanggan.DoesNotExist:
        pass

    # Try Teknisi (by username)
    try:
        teknisi = Teknisi.objects.get(username=login_id)
        if teknisi.check_password(password):
            request.session['teknisi_id'] = teknisi.id_teknisi
            request.session['user_role'] = teknisi.role_akses or 'teknisi'
            return Response({'message': 'Login berhasil', 'user': {'role': teknisi.role_akses, 'id': teknisi.id_teknisi, 'nama': teknisi.nama_teknisi}}, status=status.HTTP_200_OK)

        # Teknisi legacy fallbacks
        tph = getattr(teknisi, 'password_hash', None)
        if tph:
            if tph == password or hashlib.md5(password.encode('utf-8')).hexdigest() == tph:
                try:
                    teknisi.set_password(password)
                    teknisi.save()
                except Exception:
                    pass
                request.session['teknisi_id'] = teknisi.id_teknisi
                request.session['user_role'] = teknisi.role_akses or 'teknisi'
                return Response({'message': 'Login berhasil (legacy)', 'user': {'role': teknisi.role_akses, 'id': teknisi.id_teknisi, 'nama': teknisi.nama_teknisi}}, status=status.HTTP_200_OK)
    except Teknisi.DoesNotExist:
        pass

    return Response({'error': 'Email/username atau password salah'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@csrf_exempt
def registrasi_pelanggan(request):
    # GET -> render halaman registrasi (template)
    if request.method == 'GET':
        return render(request, 'register.html')

    # POST -> terima data registrasi (JSON) dan simpan ke DB
    serializer = PelangganRegistrasiSerializer(data=request.data)
    if serializer.is_valid():
        pelanggan = serializer.save()
        return Response({
            'message': 'Registrasi berhasil',
            'pelanggan': PelangganSerializer(pelanggan).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_pemesanan(request):
    if request.method == 'GET':
        id_pelanggan = request.GET.get('id_pelanggan')
        if not id_pelanggan:
            return Response({'error': 'id_pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

        pemesanan = PemesananJasa.objects.filter(id_pelanggan=id_pelanggan).order_by('-tanggal_pemesanan')
        serializer = PemesananJasaSerializer(pemesanan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PemesananJasaCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Set status awal saat menyimpan
            pemesanan = serializer.save(status_pemesanan='Menunggu Penugasan')
            
            # (Logika Notifikasi dihapus karena tabel Notifikasi tidak ada di .sql)
            
            return Response({
                'message': 'Pemesanan berhasil dibuat',
                'pemesanan': PemesananJasaSerializer(pemesanan).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_speed_test(request):
    serializer = RiwayatTestingWifiCreateSerializer(data=request.data)
    if serializer.is_valid():
        testing = serializer.save()
        
        # (Logika Notifikasi dihapus)

        return Response({
            'message': 'Data speed test berhasil disimpan',
            'testing': RiwayatTestingWifiSerializer(testing).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_dashboard(request):
    id_pelanggan = request.GET.get('id_pelanggan')
    if not id_pelanggan:
        return Response({'error': 'id_pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pelanggan = Pelanggan.objects.get(id_pelanggan=id_pelanggan)
        langganan = Langganan.objects.filter(id_pelanggan=id_pelanggan).first()
        paket = PaketLayanan.objects.filter(id_paket=langganan.id_paket).first() if langganan else None

        data = {
            'user': PelangganSerializer(pelanggan).data,
            'subscription': {
                'paket_name': paket.nama_paket if paket else 'Belum berlangganan',
                'kecepatan': f"{paket.kecepatan_mbps} Mbps" if paket else '-',
                'status': 'Aktif' if langganan and langganan.status_berlangganan == 'AKTIF' else 'Tidak Aktif',
                'tanggal_berakhir': langganan.tanggal_berakhir.strftime('%d/%m/%Y') if langganan else '-'
            },
            'recent_services': PemesananJasaSerializer(
                PemesananJasa.objects.filter(id_pelanggan=id_pelanggan).order_by('-tanggal_pemesanan')[:5],
                many=True
            ).data
        }
        return Response(data, status=status.HTTP_200_OK)

    except Pelanggan.DoesNotExist:
        return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def teknisi_tugas(request):
    id_teknisi = request.GET.get('id_teknisi')
    if not id_teknisi:
        return Response({'error': 'id_teknisi diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    tugas = PemesananJasa.objects.filter(
        id_teknisi=id_teknisi
    ).exclude(
        status_pemesanan='Selesai'
    ).order_by('-tanggal_pemesanan')

    serializer = PemesananJasaSerializer(tugas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def teknisi_update_status(request, id_pemesanan):
    try:
        pemesanan = PemesananJasa.objects.get(id_pemesanan=id_pemesanan)
    except PemesananJasa.DoesNotExist:
        return Response({'error': 'Pemesanan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

    status_baru = request.data.get('status_pemesanan')
    # Validasi status baru sesuai ENUM di .sql Anda
    valid_status = ['Menunggu Penugasan', 'Ditugaskan', 'Dikerjakan', 'Selesai', 'Batal']
    
    if status_baru and status_baru in valid_status:
        pemesanan.status_pemesanan = status_baru
        pemesanan.save()
        
        # (Logika Notifikasi dihapus)

        return Response({
            'message': 'Status pemesanan berhasil diperbarui',
            'pemesanan': PemesananJasaSerializer(pemesanan).data
        }, status=status.HTTP_200_OK)

    return Response({'error': f'status_pemesanan diperlukan dan harus salah satu dari: {valid_status}'}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint teknisi_laporan dihapus karena tabel LaporanTeknisi tidak ada di .sql


@api_view(['GET'])
def admin_pemesanan_menunggu(request):
    pemesanan = PemesananJasa.objects.filter(
        status_pemesanan='Menunggu Penugasan'
    ).order_by('tanggal_pemesanan')

    serializer = PemesananJasaSerializer(pemesanan, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def admin_tugaskan_teknisi(request):
    id_pemesanan = request.data.get('id_pemesanan')
    id_teknisi = request.data.get('id_teknisi')

    if not id_pemesanan or not id_teknisi:
        return Response({'error': 'id_pemesanan dan id_teknisi diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        pemesanan = PemesananJasa.objects.get(id_pemesanan=id_pemesanan)
        teknisi = Teknisi.objects.get(id_teknisi=id_teknisi)

        # !!! LOGIKA DIUBAH !!!
        # .sql Anda tidak punya status_ketersediaan, jadi pengecekan itu dihapus.
        # Kita langsung tugaskan saja.

        pemesanan.id_teknisi = teknisi
        pemesanan.status_pemesanan = 'Ditugaskan'
        pemesanan.save()

        # (Logika Notifikasi dihapus)

        return Response({
            'message': 'Teknisi berhasil ditugaskan',
            'pemesanan': PemesananJasaSerializer(pemesanan).data
        }, status=status.HTTP_200_OK)

    except PemesananJasa.DoesNotExist:
        return Response({'error': 'Pemesanan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
    except Teknisi.DoesNotExist:
        return Response({'error': 'Teknisi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def admin_list_teknisi(request):
    # Mengganti admin_teknisi_tersedia karena tidak ada status ketersediaan
    teknisi = Teknisi.objects.all()
    serializer = TeknisiSerializer(teknisi, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def admin_paket_layanan(request, id_paket=None):
    # Endpoint ini seharusnya masih bekerja, hanya menyesuaikan nama field
    if request.method == 'GET':
        if id_paket:
            try:
                paket = PaketLayanan.objects.get(id_paket=id_paket)
                serializer = PaketLayananSerializer(paket)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PaketLayanan.DoesNotExist:
                return Response({'error': 'Paket tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        else:
            paket = PaketLayanan.objects.all()
            serializer = PaketLayananSerializer(paket, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PaketLayananSerializer(data=request.data)
        if serializer.is_valid():
            paket = serializer.save()
            return Response({
                'message': 'Paket layanan berhasil dibuat',
                'paket': PaketLayananSerializer(paket).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not id_paket:
            return Response({'error': 'id_paket diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            paket = PaketLayanan.objects.get(id_paket=id_paket)
        except PaketLayanan.DoesNotExist:
            return Response({'error': 'Paket tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaketLayananSerializer(paket, data=request.data, partial=True)
        if serializer.is_valid():
            paket = serializer.save()
            return Response({
                'message': 'Paket layanan berhasil diperbarui',
                'paket': PaketLayananSerializer(paket).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not id_paket:
            return Response({'error': 'id_paket diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            paket = PaketLayanan.objects.get(id_paket=id_paket)
            paket.delete()
            return Response({'message': 'Paket layanan berhasil dihapus'}, status=status.HTTP_200_OK)
        except PaketLayanan.DoesNotExist:
            return Response({'error': 'Paket tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_langganan(request):
    id_pelanggan = request.GET.get('id_pelanggan')
    if not id_pelanggan:
        return Response({'error': 'id_pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    langganan = Langganan.objects.filter(id_pelanggan=id_pelanggan).order_by('-tanggal_mulai')
    serializer = LanggananSerializer(langganan, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Endpoint Notifikasi, Tagihan, dan Laporan dihapus karena tabelnya tidak ada di .sql


@api_view(['GET'])
def user_riwayat_testing(request):
    id_pelanggan = request.GET.get('id_pelanggan')
    if not id_pelanggan:
        return Response({'error': 'id_pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

    riwayat = RiwayatTestingWifi.objects.filter(
        id_langganan__id_pelanggan=id_pelanggan
    ).order_by('-waktu_testing')

    serializer = RiwayatTestingWifiSerializer(riwayat, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def admin_dashboard_stats(request):
    total_pelanggan = Pelanggan.objects.count() # .sql tidak punya status_aktif
    total_teknisi = Teknisi.objects.count()
    # .sql tidak punya teknisi_tersedia
    pemesanan_menunggu = PemesananJasa.objects.filter(status_pemesanan='Menunggu Penugasan').count()
    langganan_aktif = Langganan.objects.filter(status_langganan='Aktif').count()

    return Response({
        'total_pelanggan': total_pelanggan,
        'total_teknisi': total_teknisi,
        'teknisi_tersedia': "N/A", # Dihapus karena .sql tidak mendukung
        'pemesanan_menunggu': pemesanan_menunggu,
        'langganan_aktif': langganan_aktif
    }, status=status.HTTP_200_OK)


# def dashboard_pelanggan_view(request):
#     """Session-aware dashboard view for pelanggan.
#     The login() view sets request.session['pelanggan_id'] on successful login.
#     """
#     pelanggan_id = request.session.get('pelanggan_id')
#     if not pelanggan_id:
#         return redirect('login')

#     try:
#         pelanggan = Pelanggan.objects.get(id_pelanggan=pelanggan_id)
#     except Pelanggan.DoesNotExist:
#         return redirect('login')

#     langganan = Langganan.objects.filter(id_pelanggan=pelanggan).order_by('-tanggal_mulai').first()
#     riwayat_test = RiwayatTestingWifi.objects.filter(id_langganan__id_pelanggan=pelanggan_id).order_by('-waktu_testing')[:5]
#     pemesanan_terakhir = PemesananJasa.objects.filter(id_pelanggan=pelanggan).order_by('-tanggal_pemesanan')[:5]

#     # Build context matching template variable names
#     user_ctx = {
#         'nama': getattr(pelanggan, 'nama_lengkap', '') or getattr(pelanggan, 'nama', ''),
#         'email': getattr(pelanggan, 'email', ''),
#         'no_telp': getattr(pelanggan, 'no_telepon', '') or getattr(pelanggan, 'no_telp', ''),
#         'alamat': getattr(pelanggan, 'alamat_pemasangan', '') or getattr(pelanggan, 'alamat', ''),
#     }

#     paket = None
#     if langganan and hasattr(langganan, 'id_paket'):
#         paket = langganan.id_paket

#     subscription_ctx = {
#         'paket_name': getattr(paket, 'nama_paket', '') if paket else 'Belum berlangganan',
#         'kecepatan': f"{getattr(paket, 'kecepatan_mbps', '-') } Mbps" if paket else '-',
#         'status': 'Aktif' if langganan and getattr(langganan, 'status_langganan', '').lower() == 'aktif' else 'Tidak Aktif'
#     }

#     recent_services = []
#     for s in pemesanan_terakhir:
#         jenis = ''
#         try:
#             jenis = s.id_jenis_jasa.nama_jasa
#         except Exception:
#             jenis = getattr(s, 'jenis_jasa', '') or ''
#         recent_services.append({
#             'jenis_jasa': jenis,
#             'tanggal_pemesanan': getattr(s, 'tanggal_pemesanan', None),
#             'status_pemesanan': getattr(s, 'status_pemesanan', '')
#         })

#     context = {
#         'user': user_ctx,
#         'subscription': subscription_ctx,
#         'recent_services': recent_services,
#     }
#     return render(request, 'user/dashboard.html', context)