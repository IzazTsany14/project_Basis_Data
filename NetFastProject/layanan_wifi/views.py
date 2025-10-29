# GANTI SEMUA ISI views.py DENGAN INI:

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, date

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
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    login_id = serializer.validated_data['login_id']
    password = serializer.validated_data['password']

    user_data = None
    
    # 1. Coba login sebagai Pelanggan (via email)
    try:
        user = Pelanggan.objects.get(email=login_id)
        if user.check_password(password):
            user_data = PelangganSerializer(user).data
            user_data['role'] = 'pelanggan'
    except Pelanggan.DoesNotExist:
        pass # Lanjut ke pengecekan teknisi

    # 2. Jika bukan pelanggan, coba login sebagai Teknisi/Admin (via username)
    if not user_data:
        try:
            user = Teknisi.objects.get(username=login_id)
            if user.check_password(password):
                user_data = TeknisiSerializer(user).data
                user_data['role'] = user.role_akses # 'Teknisi' atau 'Admin'
        except Teknisi.DoesNotExist:
            pass # Tidak ditemukan

    # 3. Evaluasi hasil
    if user_data:
        return Response({
            'message': 'Login berhasil',
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        # Jika user_data masih None, berarti login_id atau password salah
        return Response({
            'error': 'Kombinasi ID Login (email/username) dan password salah.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registrasi_pelanggan(request):
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