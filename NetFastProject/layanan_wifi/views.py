from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from datetime import datetime, date
import hashlib
from django.http import JsonResponse

from .models import (
    Pelanggan, Teknisi, PaketLayanan, Langganan,
    PemesananJasa, RiwayatTestingWifi, AreaLayanan
)
from .serializers import (
    PelangganSerializer, PelangganRegistrasiSerializer, TeknisiSerializer,
    PaketLayananSerializer, LanggananSerializer,
    PemesananJasaSerializer, PemesananJasaCreateSerializer,
    RiwayatTestingWifiSerializer,
    RiwayatTestingWifiCreateSerializer, LoginSerializer, AreaLayananSerializer
)

# --- LOGIKA BARU UNTUK LOGIN ---
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import role_required

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect to the generic dashboard dispatcher
    return render(request, 'index.html')

def logout(request):
    # Clear custom session flags and Django auth
    request.session.flush() # More thorough than popping individual keys
    try:
        auth_logout(request)
    except Exception:
        pass
    # Return a simple JSON response so frontend can react
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
    
def dashboard_redirect_view(request):
    user_role = request.session.get('user_role')

    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'teknisi':
        return redirect('teknisi_dashboard')
    elif user_role == 'pelanggan':
        return redirect('user_dashboard') # Assuming 'user_dashboard' is the name for pelanggan dashboard
    else:
        # Fallback if role is not recognized or not set
        return redirect('login')

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
        'tanggal_bergabung': getattr(pelanggan, 'tanggal_bergabung', None),
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
        'recent_tests': riwayat_test,
    }
    return render(request, 'user/dashboard.html', context)

# --- Admin Views (from HEAD) ---
@role_required(allowed_roles=['admin'])
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')

@role_required(allowed_roles=['admin'])
def admin_manajemen_pesanan_view(request):
    return render(request, 'admin/manajemen-pesanan.html')

@role_required(allowed_roles=['admin'])
def admin_manajemen_teknisi_view(request):
    return render(request, 'admin/manajemen-teknisi.html')

@role_required(allowed_roles=['admin'])
def admin_manajemen_pelanggan_view(request):
    return render(request, 'admin/manajemen-pelanggan.html')

# --- Teknisi Views (from HEAD) ---
@role_required(allowed_roles=['teknisi', 'admin'])
def teknisi_dashboard_view(request):
    return render(request, 'teknisi/dashboard.html')

@role_required(allowed_roles=['teknisi', 'admin'])
def teknisi_detail_tugas_view(request):
    return render(request, 'teknisi/detail-tugas.html')

@role_required(allowed_roles=['teknisi', 'admin'])
def teknisi_edit_profile_view(request):
    """Render halaman edit profil untuk teknisi.
    Template: templates/teknisi/edit-profile.html
    """
    teknisi_id = request.session.get('teknisi_id')
    if not teknisi_id:
        return redirect('login_page')
    
    try:
        teknisi = Teknisi.objects.get(id_teknisi=teknisi_id)
    except Teknisi.DoesNotExist:
        return redirect('login_page')
    
    context = {
        'user': {
            'nama': teknisi.nama_teknisi,
            'username': teknisi.username,
            'area_layanan': getattr(teknisi.id_area_layanan, 'nama_area', '') if teknisi.id_area_layanan else '',
            'no_telepon': getattr(teknisi, 'no_telepon', ''),
            'alamat': getattr(teknisi, 'alamat', '')
        }
    }
    return render(request, 'teknisi/edit-profile.html', context)

# --- Pelanggan Views (from ecdb7c0...) ---
def speed_test_view(request):
    """Render halaman speed test untuk pelanggan.
    Template: templates/user/speed-test.html
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')
    return render(request, 'user/speed-test.html')

def edit_profile_view(request):
    """Render halaman edit profil untuk pelanggan.
    Template: templates/user/edit-profile.html
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')
    
    try:
        pelanggan = Pelanggan.objects.get(id_pelanggan=pelanggan_id)
    except Pelanggan.DoesNotExist:
        return redirect('login')
    
    context = {
        'user': {
            'nama': pelanggan.nama_lengkap,
            'email': pelanggan.email,
            'no_telp': pelanggan.no_telepon,
            'alamat': pelanggan.alamat_pemasangan
        }
    }
    return render(request, 'user/edit-profile.html', context)

def packages_view(request):
    """Render halaman paket internet untuk pelanggan.
    Template: templates/user/packages.html
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')

    try:
        # Ambil paket aktif pelanggan
        langganan = Langganan.objects.filter(
            id_pelanggan=pelanggan_id,
            status_langganan='AKTIF'
        ).latest('tanggal_mulai')
        current_package_id = langganan.id_paket.id_paket
    except Langganan.DoesNotExist:
        current_package_id = None
    
    context = {
        'currentPackageId': current_package_id
    }
    return render(request, 'user/packages.html', context)

def services_history_view(request):
    """Render halaman riwayat layanan untuk pelanggan.
    Template: templates/user/services-history.html
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')
    return render(request, 'user/services-history.html')


def speed_history_view(request):
    """Render halaman riwayat uji kecepatan (grafik) untuk pelanggan.
    Template: templates/user/speed-history.html
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return redirect('login')
    return render(request, 'user/speed-history.html')

# --- Sisa Kode (API Views, dll) ---

@api_view(['POST'])
@csrf_exempt
def login(request):
    from rest_framework.parsers import FormParser, MultiPartParser
    request.parsers = [FormParser(), MultiPartParser()]
    # Accept {login_id, password}
    data = request.POST
    password = data.get('password')
    login_id = data.get('login_id') or data.get('email') or data.get('username')

    if not login_id or not password:
        return JsonResponse({'error': 'login_id dan password diperlukan'}, status=400)

    # Try Admin first (by username, role_akses = 'admin')
    try:
        admin_user = Teknisi.objects.get(username=login_id, role_akses='admin')
        if admin_user.check_password(password):
            request.session['teknisi_id'] = admin_user.id_teknisi
            request.session['user_role'] = 'admin'
            request.session.cycle_key()
            request.session.save()
            return JsonResponse({'message': 'Login berhasil', 'user': {'role': 'admin', 'id': admin_user.id_teknisi, 'nama': admin_user.nama_teknisi}}, status=200)

        # Admin legacy fallbacks
        aph = getattr(admin_user, 'password_hash', None)
        if aph:
            if aph == password or hashlib.md5(password.encode('utf-8')).hexdigest() == aph:
                try:
                    admin_user.set_password(password)
                    admin_user.save()
                except Exception:
                    pass
                request.session['teknisi_id'] = admin_user.id_teknisi
                request.session['user_role'] = 'admin'
                request.session.cycle_key()
                request.session.save()
                return JsonResponse({'message': 'Login berhasil (legacy)', 'user': {'role': 'admin', 'id': admin_user.id_teknisi, 'nama': admin_user.nama_teknisi}}, status=200)
    except Teknisi.DoesNotExist:
        pass

    # Try Teknisi (by username, exclude admin)
    try:
        teknisi = Teknisi.objects.exclude(role_akses='admin').get(username=login_id)
        if teknisi.check_password(password):
            request.session['teknisi_id'] = teknisi.id_teknisi
            request.session['user_role'] = 'teknisi'
            request.session.cycle_key()
            request.session.save()
            return JsonResponse({'message': 'Login berhasil', 'user': {'role': 'teknisi', 'id': teknisi.id_teknisi, 'nama': teknisi.nama_teknisi}}, status=200)

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
                request.session['user_role'] = 'teknisi'
                request.session.cycle_key()
                request.session.save()
                return JsonResponse({'message': 'Login berhasil (legacy)', 'user': {'role': 'teknisi', 'id': teknisi.id_teknisi, 'nama': teknisi.nama_teknisi}}, status=200)
    except Teknisi.DoesNotExist:
        pass

    # Try Pelanggan (by email)
    try:
        pelanggan = Pelanggan.objects.get(email=login_id)
        # Normal Django-hashed password
        if pelanggan.check_password(password):
            request.session['pelanggan_id'] = pelanggan.id_pelanggan
            request.session['user_role'] = 'pelanggan'
            request.session.save()
            return JsonResponse({'message': 'Login berhasil', 'user': {'role': 'pelanggan', 'id': pelanggan.id_pelanggan, 'nama': getattr(pelanggan, 'nama_lengkap', '')}}, status=200)

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
            return JsonResponse({'message': 'Login berhasil (legacy) - password upgraded', 'user': {'role': 'pelanggan', 'id': pelanggan.id_pelanggan, 'nama': getattr(pelanggan, 'nama_lengkap', '')}}, status=200)
    except Pelanggan.DoesNotExist:
        pass

    return JsonResponse({'error': 'Email/username atau password salah'}, status=401)


@api_view(['POST'])
@csrf_exempt
def login_api(request):
    # Accept either {email,password} or {username,password} or {login_id,password}
    data = request.data if isinstance(request.data, dict) else {}
    password = data.get('password')
    login_id = data.get('login_id') or data.get('email') or data.get('username')


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
        # Create default subscription or handle as needed
        # For now, just register the user
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
        # Get pelanggan_id from session
        pelanggan_id = request.session.get('pelanggan_id')
        if not pelanggan_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['id_pelanggan'] = pelanggan_id

        serializer = PemesananJasaCreateSerializer(data=data)
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
    id_teknisi = request.session.get('teknisi_id') # Changed from request.GET
    if not id_teknisi:
        return Response({'error': 'Sesi teknisi tidak ditemukan atau tidak valid'}, status=status.HTTP_401_UNAUTHORIZED)

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
    ).select_related('id_pelanggan', 'id_jenis_jasa').order_by('-tanggal_pemesanan')

    serializer = PemesananJasaSerializer(pemesanan, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def admin_pesanan_aktif(request):
    pemesanan = PemesananJasa.objects.exclude(
        status_pemesanan='Menunggu Penugasan'
    ).exclude(
        status_pemesanan='Selesai'
    ).exclude(
        status_pemesanan='Batal'
    ).select_related('id_pelanggan', 'id_jenis_jasa', 'id_teknisi').order_by('-tanggal_pemesanan')

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
    teknisi = Teknisi.objects.all().order_by('nama_teknisi')
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


@api_view(['GET', 'POST'])
def speed_test_api(request):
    """
    GET: Ambil riwayat testing terakhir
    POST: Simpan hasil speed test baru
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        # Ambil semua riwayat testing untuk pelanggan ini dari semua langganan
        langganan_ids = Langganan.objects.filter(id_pelanggan=pelanggan_id).values_list('id_langganan', flat=True)
        riwayat = RiwayatTestingWifi.objects.filter(
            id_langganan__in=langganan_ids
        ).order_by('-waktu_testing')[:10]  # 10 tes terakhir

        serializer = RiwayatTestingWifiSerializer(riwayat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Validasi data tes
        data = request.data
        if not all(key in data for key in ['download_speed_mbps', 'upload_speed_mbps', 'ping_ms']):
            return Response({'error': 'Semua parameter speed test diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
<<<<<<< HEAD

        # Validate speeds against package speed
        package_speed = paket.kecepatan_mbps
        measured_speed = float(data['download_speed_mbps'])
=======
>>>>>>> 5871e0f2112f2a668ba64d308a3c3aa076281f3f

        try:
            # Coba ambil langganan aktif jika ada (opsional)
            langganan = None
            try:
                langganan = Langganan.objects.filter(
                    id_pelanggan=pelanggan_id,
                    status_langganan='AKTIF'
                ).latest('tanggal_mulai')

                # Log perbandingan dengan paket jika ada langganan aktif
                if langganan.id_paket:
                    package_speed = langganan.id_paket.kecepatan_mbps
                    measured_speed = float(data['download_speed_mbps'])
                    print(f"Package speed: {package_speed} Mbps, Measured: {measured_speed} Mbps")

            except Langganan.DoesNotExist:
                # Tidak ada langganan aktif, tapi tetap izinkan tes kecepatan
                print(f"No active subscription for pelanggan {pelanggan_id}, but allowing speed test anyway")

            # Deteksi tipe koneksi
            connection_type = data.get('connection_type', 'Unknown')
            if not connection_type or connection_type == 'Unknown':
                # Coba deteksi otomatis berdasarkan kecepatan
                download_speed = float(data['download_speed_mbps'])
                if download_speed >= 100:
                    connection_type = 'Fiber Optic'
                elif download_speed >= 50:
                    connection_type = 'Cable Broadband'
                elif download_speed >= 25:
                    connection_type = 'DSL'
                elif download_speed >= 10:
                    connection_type = 'Mobile Data'
                else:
                    connection_type = 'Slow Connection'

            # Simpan hasil tes ke database (id_langganan bisa null)
            test = RiwayatTestingWifi.objects.create(
<<<<<<< HEAD
                id_langganan=langganan,
=======
                id_langganan=langganan,  # Bisa None jika tidak ada langganan aktif
>>>>>>> 5871e0f2112f2a668ba64d308a3c3aa076281f3f
                download_speed_mbps=float(data['download_speed_mbps']),
                upload_speed_mbps=float(data['upload_speed_mbps']),
                ping_ms=int(data['ping_ms']),
                waktu_testing=datetime.now()
            )

            serializer = RiwayatTestingWifiSerializer(test)
            return Response({
                'message': 'Speed test berhasil disimpan ke riwayat',
                'test': serializer.data
            }, status=status.HTTP_201_CREATED)

        except (ValueError, TypeError):
            return Response({'error': 'Format data speed test tidak valid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Gagal menyimpan speed test: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


@api_view(['GET', 'POST'])
def profile_api(request):
    """
    GET: Ambil data profil user
    POST: Update data profil user
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        pelanggan = Pelanggan.objects.get(id_pelanggan=pelanggan_id)
    except Pelanggan.DoesNotExist:
        return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

    try:
        pelanggan = Pelanggan.objects.get(id_pelanggan=pelanggan_id)
    except Pelanggan.DoesNotExist:
        return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PelangganSerializer(pelanggan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        update_fields = []
        
        # Validate required fields
        required_fields = ['nama_lengkap', 'email', 'no_telepon', 'alamat_pemasangan']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'error': f'Field {field} harus diisi'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Update customer data
        if 'nama_lengkap' in data:
            pelanggan.nama_lengkap = data['nama_lengkap']
            update_fields.append('nama_lengkap')

        if 'email' in data:
            if data['email'] != pelanggan.email:
                # Cek email unik
                if Pelanggan.objects.filter(email=data['email']).exists():
                    return Response({'error': 'Email sudah digunakan'}, status=status.HTTP_400_BAD_REQUEST)
                pelanggan.email = data['email']
                update_fields.append('email')

        if 'no_telepon' in data:
            pelanggan.no_telepon = data['no_telepon']
            update_fields.append('no_telepon')

        if 'alamat_pemasangan' in data:
            pelanggan.alamat_pemasangan = data['alamat_pemasangan']
            update_fields.append('alamat_pemasangan')

        if update_fields:
            try:
                pelanggan.save(update_fields=update_fields)
                return Response({
                    'message': 'Profil berhasil diperbarui',
                    'user': PelangganSerializer(pelanggan).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Tidak ada data yang diperbarui'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def teknisi_profile_api(request):
    """
    GET: Ambil data profil teknisi
    POST: Update data profil teknisi
    """
    teknisi_id = request.session.get('teknisi_id')
    if not teknisi_id:
        return Response({'success': False, 'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        teknisi = Teknisi.objects.get(id_teknisi=teknisi_id)
    except Teknisi.DoesNotExist:
        return Response({'success': False, 'error': 'Teknisi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({
            'success': True,
            'nama': teknisi.nama_teknisi,
            'username': teknisi.username,
            'area_layanan': getattr(teknisi.id_area_layanan, 'nama_area', '') if teknisi.id_area_layanan else '',
            'no_telepon': getattr(teknisi, 'no_telepon', ''),
            'alamat': getattr(teknisi, 'alamat', '')
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Update teknisi profile
        if 'nama' in request.data:
            teknisi.nama_teknisi = request.data['nama']
        
        if 'no_telepon' in request.data:
            teknisi.no_telepon = request.data['no_telepon']
        
        if 'alamat' in request.data:
            teknisi.alamat = request.data['alamat']
        
        if 'password' in request.data and request.data['password']:
            teknisi.set_password(request.data['password'])
        
        try:
            teknisi.save()
            return Response({
                'success': True,
                'message': 'Profil berhasil diperbarui'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def service_detail_api(request, service_id):
    """API endpoint to get specific service details"""
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        service = PemesananJasa.objects.get(
            id_pemesanan=service_id,
            id_pelanggan=pelanggan_id
        )
        serializer = PemesananJasaSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PemesananJasa.DoesNotExist:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def package_api(request):
    """
    GET: Ambil data paket aktif dan daftar paket tersedia
    POST: Ganti paket berlangganan
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        # Ambil paket aktif
        try:
            langganan = Langganan.objects.filter(
                id_pelanggan=pelanggan_id,
                status_langganan='AKTIF'
            ).latest('tanggal_mulai')
            current_package = PaketLayananSerializer(langganan.id_paket).data
        except Langganan.DoesNotExist:
            current_package = None

        # Ambil semua paket tersedia
        all_packages = PaketLayanan.objects.all()
        packages = PaketLayananSerializer(all_packages, many=True).data

        return Response({
            'current_package': current_package,
            'available_packages': packages
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        package_id = request.data.get('package_id')
        if not package_id:
            return Response({'error': 'ID paket diperlukan'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validasi paket baru
            new_package = PaketLayanan.objects.get(id_paket=package_id)

            # Nonaktifkan langganan lama jika ada
            Langganan.objects.filter(
                id_pelanggan=pelanggan_id,
                status_langganan='AKTIF'
            ).update(
                status_langganan='NONAKTIF',
                tanggal_akhir=date.today()
            )

            # Buat langganan baru
            langganan = Langganan.objects.create(
                id_pelanggan_id=pelanggan_id,
                id_paket=new_package,
                tanggal_mulai=date.today(),
                status_langganan='AKTIF'
            )

            return Response({
                'message': 'Paket berhasil diubah',
                'subscription': LanggananSerializer(langganan).data
            }, status=status.HTTP_201_CREATED)

        except PaketLayanan.DoesNotExist:
            return Response({'error': 'Paket tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete_package_api(request):
    """
    POST: Hapus paket aktif (nonaktifkan langganan)
    """
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Nonaktifkan langganan aktif
        updated_count = Langganan.objects.filter(
            id_pelanggan=pelanggan_id,
            status_langganan='AKTIF'
        ).update(
            status_langganan='NONAKTIF',
            tanggal_akhir=date.today()
        )

        if updated_count == 0:
            return Response({'error': 'Tidak ada paket aktif yang dapat dihapus'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Paket berhasil dihapus',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def services_list_api(request):
    """API endpoint to get user's service history"""
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        services = PemesananJasa.objects.filter(
            id_pelanggan=pelanggan_id
        ).order_by('-tanggal_pemesanan')
        
        serializer = PemesananJasaSerializer(services, many=True)
        return Response({
            'services': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def ping_test_api(request):
    """
    Endpoint for ping testing
    """
    import time
    import urllib.request
    start = time.time()
    try:
        # Use urllib to make a simple HTTP request
        req = urllib.request.Request('https://www.google.com', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            end = time.time()
            ping_ms = int((end - start) * 1000)
            return Response({'ping_ms': ping_ms}, status=status.HTTP_200_OK)
    except Exception as e:
        # Fallback ping value if request fails
        return Response({'ping_ms': 50}, status=status.HTTP_200_OK)

@api_view(['POST'])
def speed_test_upload(request):
    """
    Endpoint for upload speed testing
    """
    try:
        # Validate that we received data
        if not request.body:
            return Response({'error': 'No data received'}, status=status.HTTP_400_BAD_REQUEST)

        # Log upload details for debugging
        upload_size = len(request.body)
        print(f"Upload test received: {upload_size} bytes")

        # Return success response with timing info
        return Response({
            'message': 'Upload received',
            'bytes_received': upload_size,
            'timestamp': datetime.now().isoformat()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Upload test error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def services_history_api(request):
    """API endpoint for user's service history"""
    pelanggan_id = request.session.get('pelanggan_id')
    if not pelanggan_id:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    try:
        # Get all services with related data
        services = PemesananJasa.objects.filter(
            id_pelanggan=pelanggan_id
        ).select_related(
            'id_jenis_jasa',
            'id_teknisi'
        ).order_by('-tanggal_pemesanan')
        
        serializer = PemesananJasaSerializer(services, many=True)
        return Response({
            'services': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def admin_dashboard_stats(request):
    total_pelanggan = Pelanggan.objects.count() # Total customers
    total_teknisi = Teknisi.objects.count() # Total technicians
    pemesanan_baru = PemesananJasa.objects.count() # All orders as "new orders"
    langganan_aktif = Langganan.objects.filter(status_langganan='AKTIF').count() # Active subscriptions

    return Response({
        'total_pelanggan': total_pelanggan,
        'total_teknisi': total_teknisi,
        'pemesanan_menunggu': pemesanan_baru,  # Changed to all orders
        'langganan_aktif': langganan_aktif
    }, status=status.HTTP_200_OK)
<<<<<<< HEAD





@api_view(['GET'])
def admin_dashboard_chart(request):
    """Endpoint untuk data chart dashboard admin - pelanggan baru dan pesanan per bulan"""
    from django.db.models.functions import TruncMonth
    from django.db.models import Count
    from datetime import timedelta
    import calendar

    # Data pelanggan baru per bulan (6 bulan terakhir)
    six_months_ago = date.today() - timedelta(days=180)
    new_customers = (
        Pelanggan.objects.filter(tanggal_daftar__gte=six_months_ago)
        .annotate(month=TruncMonth('tanggal_daftar'))
        .values('month')
        .annotate(count=Count('id_pelanggan'))
        .order_by('month')
    )

    # Data pesanan baru per bulan (6 bulan terakhir)
    new_orders = (
        PemesananJasa.objects.filter(tanggal_pemesanan__gte=six_months_ago)
        .annotate(month=TruncMonth('tanggal_pemesanan'))
        .values('month')
        .annotate(count=Count('id_pemesanan'))
        .order_by('month')
    )

    # Siapkan data untuk 6 bulan terakhir
    months = []
    customer_data = []
    order_data = []

    for i in range(5, -1, -1):
        month_date = date.today() - timedelta(days=30 * i)
        month_name = calendar.month_name[month_date.month] + ' ' + str(month_date.year)
        months.append(month_name)

        # Cari data pelanggan untuk bulan ini
        customer_count = 0
        for item in new_customers:
            if item['month'].year == month_date.year and item['month'].month == month_date.month:
                customer_count = item['count']
                break
        customer_data.append(customer_count)

        # Cari data pesanan untuk bulan ini
        order_count = 0
        for item in new_orders:
            if item['month'].year == month_date.year and item['month'].month == month_date.month:
                order_count = item['count']
                break
        order_data.append(order_count)

    return Response({
        'months': months,
        'customers': customer_data,
        'orders': order_data
    }, status=status.HTTP_200_OK)


# --- Admin Technician Management API ---
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def admin_teknisi(request, id_teknisi=None):
    if request.method == 'GET':
        if id_teknisi:
            try:
                teknisi = Teknisi.objects.get(id_teknisi=id_teknisi)
                serializer = TeknisiSerializer(teknisi)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Teknisi.DoesNotExist:
                return Response({'error': 'Teknisi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get query parameters for filtering and sorting
            search = request.GET.get('search', '')
            area_id = request.GET.get('area_id', '')
            sort_by = request.GET.get('sort_by', 'nama_teknisi')

            # Base queryset
            teknisi = Teknisi.objects.select_related('id_area_layanan')

            # Apply search filter
            if search:
                teknisi = teknisi.filter(
                    Q(nama_teknisi__icontains=search) |
                    Q(username__icontains=search)
                )

            # Apply area filter
            if area_id:
                teknisi = teknisi.filter(id_area_layanan=area_id)

            # Apply sorting
            if sort_by == 'area_layanan':
                sort_field = 'id_area_layanan__nama_area'
            elif sort_by == 'role_akses':
                sort_field = 'role_akses'
            elif sort_by == 'username':
                sort_field = 'username'
            else:
                sort_field = 'nama_teknisi'

            teknisi = teknisi.order_by(sort_field)

            serializer = TeknisiSerializer(teknisi, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        # Handle password setting for new technicians
        if 'password' in data:
            password = data.pop('password')
            serializer = TeknisiSerializer(data=data)
            if serializer.is_valid():
                teknisi = serializer.save()
                teknisi.set_password(password)
                teknisi.save()
                return Response({
                    'message': 'Teknisi berhasil dibuat',
                    'teknisi': TeknisiSerializer(teknisi).data
                }, status=status.HTTP_201_CREATED)
        else:
            serializer = TeknisiSerializer(data=data)
            if serializer.is_valid():
                teknisi = serializer.save()
                return Response({
                    'message': 'Teknisi berhasil dibuat',
                    'teknisi': TeknisiSerializer(teknisi).data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not id_teknisi:
            return Response({'error': 'ID teknisi diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teknisi = Teknisi.objects.get(id_teknisi=id_teknisi)
        except Teknisi.DoesNotExist:
            return Response({'error': 'Teknisi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeknisiSerializer(teknisi, data=request.data, partial=True)
        if serializer.is_valid():
            teknisi = serializer.save()
            return Response({
                'message': 'Teknisi berhasil diperbarui',
                'teknisi': TeknisiSerializer(teknisi).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not id_teknisi:
            return Response({'error': 'ID teknisi diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teknisi = Teknisi.objects.get(id_teknisi=id_teknisi)
            teknisi.delete()
            return Response({'message': 'Teknisi berhasil dihapus'}, status=status.HTTP_200_OK)
        except Teknisi.DoesNotExist:
            return Response({'error': 'Teknisi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)


# --- Admin Area Layanan API ---
@api_view(['GET'])
def admin_area_layanan(request):
    areas = AreaLayanan.objects.all().order_by('nama_area')
    serializer = AreaLayananSerializer(areas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# --- Admin Customer Management API ---
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def admin_pelanggan(request, id_pelanggan=None):
    if request.method == 'GET':
        if id_pelanggan:
            try:
                pelanggan = Pelanggan.objects.get(id_pelanggan=id_pelanggan)
                serializer = PelangganSerializer(pelanggan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Pelanggan.DoesNotExist:
                return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        else:
            pelanggan = Pelanggan.objects.all().order_by('-tanggal_daftar')
            serializer = PelangganSerializer(pelanggan, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        # Handle password setting for new customers
        if 'password' in data:
            password = data.pop('password')
            serializer = PelangganSerializer(data=data)
            if serializer.is_valid():
                pelanggan = serializer.save()
                pelanggan.set_password(password)
                pelanggan.save()
                return Response({
                    'message': 'Pelanggan berhasil dibuat',
                    'pelanggan': PelangganSerializer(pelanggan).data
                }, status=status.HTTP_201_CREATED)
        else:
            serializer = PelangganSerializer(data=data)
            if serializer.is_valid():
                pelanggan = serializer.save()
                return Response({
                    'message': 'Pelanggan berhasil dibuat',
                    'pelanggan': PelangganSerializer(pelanggan).data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not id_pelanggan:
            return Response({'error': 'ID pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pelanggan = Pelanggan.objects.get(id_pelanggan=id_pelanggan)
        except Pelanggan.DoesNotExist:
            return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PelangganSerializer(pelanggan, data=request.data, partial=True)
        if serializer.is_valid():
            pelanggan = serializer.save()
            return Response({
                'message': 'Pelanggan berhasil diperbarui',
                'pelanggan': PelangganSerializer(pelanggan).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not id_pelanggan:
            return Response({'error': 'ID pelanggan diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pelanggan = Pelanggan.objects.get(id_pelanggan=id_pelanggan)
            pelanggan.delete()
            return Response({'message': 'Pelanggan berhasil dihapus'}, status=status.HTTP_200_OK)
        except Pelanggan.DoesNotExist:
            return Response({'error': 'Pelanggan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)






=======
>>>>>>> 5871e0f2112f2a668ba64d308a3c3aa076281f3f
