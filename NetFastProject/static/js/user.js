// NetFast - User Module Logic
// Use same-origin base so frontend calls map to Django urlpatterns (no separate /api prefix)
const API_BASE_URL = '';
const userId = localStorage.getItem('userId');

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    

    // Setup logout button
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.clear();
            window.location.href = '/';
        });
    }

    // Load dashboard data
    loadDashboardData();

    // Set up speed test if on speed test page
    const startSpeedTest = document.getElementById('startSpeedTest');
    if (startSpeedTest) {
        startSpeedTest.addEventListener('click', runSpeedTest);
    }
});

// Load user name for sidebar
async function loadUserName() {
    const userName = localStorage.getItem('userName');
    const userNameElements = document.querySelectorAll('#user-name, #welcome-name');
    
    userNameElements.forEach(element => {
        if (element) {
            element.textContent = userName || 'Pengguna';
        }
    });
}

// Load dashboard data
async function loadDashboardData() {
    try {
        

        const response = await fetch(`${API_BASE_URL}/user/data/?id_pelanggan=${userId}`);
        const data = await response.json();

        if (response.ok) {
            // Update user info
            document.getElementById('welcomeName').textContent = `Selamat Datang, ${data.user.nama}`;
            document.getElementById('infoNama').textContent = data.user.nama;
            document.getElementById('infoEmail').textContent = data.user.email;
            document.getElementById('infoTelepon').textContent = data.user.no_telp;
            document.getElementById('infoAlamat').textContent = data.user.alamat;

            // Update package info
            document.getElementById('paketNama').textContent = data.subscription.paket_name;
            document.getElementById('paketKecepatan').textContent = data.subscription.kecepatan;
            document.getElementById('paketStatus').textContent = data.subscription.status;
            document.getElementById('paketMulai').textContent = data.subscription.tanggal_berakhir;

            // Update billing history if exists
            if (data.recent_services && data.recent_services.length > 0) {
                const billingList = document.getElementById('billingHistory').querySelector('.list-group');
                billingList.innerHTML = data.recent_services.map(service => `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <span class="fw-bold">${service.jenis_jasa}</span><br>
                            <small class="text-muted">Tanggal: ${new Date(service.tanggal_pemesanan).toLocaleDateString('id-ID')}</small>
                        </div>
                        <span class="badge bg-${service.status_pemesanan === 'Selesai' ? 'success' : 'warning'} rounded-pill">
                            ${service.status_pemesanan}
                        </span>
                    </li>
                `).join('');
            }

        } else {
            throw new Error(data.error || 'Gagal memuat data');
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Gagal memuat data dashboard: ' + error.message, 'error');
    }
}

// Load subscription information
async function loadSubscriptionInfo() {
    try {
        const response = await NetFastAuth.apiCall('/user/subscription/');
        
        if (response && response.ok) {
            const data = await response.json();
            
            document.getElementById('paket-name').textContent = data.paket_name || 'Belum berlangganan';
            document.getElementById('paket-speed').textContent = data.kecepatan || '-';
            
            const statusElement = document.getElementById('status-langganan');
            statusElement.textContent = data.status || 'Tidak aktif';
            statusElement.className = `status-badge ${data.status === 'Aktif' ? 'active' : 'inactive'}`;
            
            document.getElementById('tanggal-berakhir').textContent = data.tanggal_berakhir || '-';
        } else {
            // Show default/empty state
            setDefaultSubscriptionInfo();
        }
    } catch (error) {
        console.error('Error loading subscription:', error);
        setDefaultSubscriptionInfo();
    }
}

function setDefaultSubscriptionInfo() {
    document.getElementById('paket-name').textContent = 'Belum berlangganan';
    document.getElementById('paket-speed').textContent = '-';
    document.getElementById('status-langganan').textContent = 'Tidak aktif';
    document.getElementById('status-langganan').className = 'status-badge inactive';
    document.getElementById('tanggal-berakhir').textContent = '-';
}

// Load payment information
async function loadPaymentInfo() {
    try {
        const response = await NetFastAuth.apiCall('/user/payment-info/');
        
        if (response && response.ok) {
            const data = await response.json();
            
            document.getElementById('tagihan-bulan').textContent = formatCurrency(data.tagihan_bulan) || 'Rp 0';
            
            const statusElement = document.getElementById('status-pembayaran');
            statusElement.textContent = data.status_pembayaran || 'Belum ada tagihan';
            statusElement.className = `status-badge ${data.status_pembayaran === 'Lunas' ? 'active' : 'pending'}`;
            
            document.getElementById('jatuh-tempo').textContent = data.jatuh_tempo || '-';
        } else {
            setDefaultPaymentInfo();
        }
    } catch (error) {
        console.error('Error loading payment info:', error);
        setDefaultPaymentInfo();
    }
}

function setDefaultPaymentInfo() {
    document.getElementById('tagihan-bulan').textContent = 'Rp 0';
    document.getElementById('status-pembayaran').textContent = 'Belum ada tagihan';
    document.getElementById('status-pembayaran').className = 'status-badge pending';
    document.getElementById('jatuh-tempo').textContent = '-';
}

// Load recent services
async function loadRecentServices() {
    try {
        const response = await NetFastAuth.apiCall('/user/recent-services/');
        
        if (response && response.ok) {
            const data = await response.json();
            const container = document.getElementById('recent-services');
            
            if (data.services && data.services.length > 0) {
                container.innerHTML = data.services.map(service => `
                    <div class="service-item">
                        <strong>${service.jenis_jasa}</strong><br>
                        <small>Status: ${service.status} | ${formatDate(service.tanggal_pesanan)}</small>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p>Tidak ada layanan terbaru</p>';
            }
        }
    } catch (error) {
        console.error('Error loading recent services:', error);
    }
}

// Load service types for order form
async function loadJenisJasa() {
    try {
        const response = await NetFastAuth.apiCall('/services/types/');
        const select = document.getElementById('jenis-jasa');
        
        if (response && response.ok) {
            const data = await response.json();
            
            // Clear existing options except the first one
            select.innerHTML = '<option value="">Pilih Jenis Jasa</option>';
            
            if (data.services) {
                data.services.forEach(service => {
                    // Skip services related to location change
                    if (service.nama_jasa && (service.nama_jasa.toLowerCase().includes('lokasi') ||
                        service.nama_jasa.toLowerCase().includes('pindah'))) {
                        return;
                    }
                    const option = document.createElement('option');
                    option.value = service.id;
                    option.textContent = `${service.nama_jasa} - ${formatCurrency(service.harga)}`;
                    select.appendChild(option);
                });
            }
        } else {
            // Add default options if API fails
            addDefaultServiceOptions(select);
        }
    } catch (error) {
        console.error('Error loading service types:', error);
        addDefaultServiceOptions(document.getElementById('jenis-jasa'));
    }
}

function addDefaultServiceOptions(select) {
    const defaultServices = [
        { id: 1, name: 'Instalasi Baru', price: 150000 },
        { id: 2, name: 'Perbaikan Jaringan', price: 75000 },
        { id: 3, name: 'Upgrade Paket', price: 50000 },
        { id: 4, name: 'Maintenance Rutin', price: 100000 }
    ];
    
    select.innerHTML = '<option value="">Pilih Jenis Jasa</option>';
    defaultServices.forEach(service => {
        const option = document.createElement('option');
        option.value = service.id;
        option.textContent = `${service.name} - ${formatCurrency(service.price)}`;
        select.appendChild(option);
    });
}

// Handle service order submission
document.addEventListener('DOMContentLoaded', function() {
    const orderForm = document.getElementById('pemesanan-form');
    if (orderForm) {
        orderForm.addEventListener('submit', handleServiceOrder);
    }
});

async function handleServiceOrder(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const orderData = {
        id_pelanggan: localStorage.getItem('userId'),
        jenis_jasa_id: formData.get('jenis_jasa'),
        tanggal_jadwal: formData.get('tanggal_jadwal'),
        waktu_jadwal: formData.get('waktu_jadwal'),
        alamat_layanan: formData.get('alamat_layanan'),
        catatan: formData.get('catatan'),
        kontak_darurat: formData.get('kontak_darurat'),
        status_pemesanan: 'Menunggu Penugasan'
    };

    try {
        NetFastAuth.showLoading(event.target.querySelector('button[type="submit"]'));
        
        const response = await NetFastAuth.apiCall('/orders/', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });

        if (response && response.ok) {
            const result = await response.json();
            NetFastAuth.showAlert('Pesanan berhasil dikirim! Teknisi akan menghubungi Anda segera.', 'success');
            
            // Reset form
            event.target.reset();
            
            // Redirect to order history after 2 seconds
            setTimeout(() => {
                window.location.href = 'riwayat-pesanan.html';
            }, 2000);
        } else {
            const error = await response.json();
            NetFastAuth.showAlert(error.message || 'Gagal mengirim pesanan. Silakan coba lagi.', 'error');
        }
    } catch (error) {
        console.error('Error submitting order:', error);
        NetFastAuth.showAlert('Terjadi kesalahan. Silakan coba lagi.', 'error');
    } finally {
        NetFastAuth.hideLoading(event.target.querySelector('button[type="submit"]'));
    }
}

// Load orders history
async function loadOrdersHistory() {
    try {
        const response = await NetFastAuth.apiCall('/user/orders/');
        const tbody = document.getElementById('orders-tbody');
        
        if (response && response.ok) {
            const data = await response.json();
            
            console.log('loadOrdersHistory:', data);
            if (data.orders && data.orders.length > 0) {
                tbody.innerHTML = data.orders.map(order => {
                    // determine payment actions: prefer to use payment_id if provided by API
                    const paymentId = order.payment_id || order.id_pembayaran || null;
                    let paymentActionBtn = '';

                    if (paymentId) {
                        // show upload button if payment still pending or not paid
                        const status = (order.payment_status || '').toLowerCase();
                        if (status.includes('menunggu') || status.includes('belum') || status.includes('pending')) {
                            paymentActionBtn = `<button class="btn-primary" onclick="openUploadFormFor(${paymentId})">Unggah Bukti</button>`;
                        } else if (status.includes('lunas') || status.includes('bayar')) {
                            paymentActionBtn = `<button class="btn-outline" onclick="openUploadFormFor(${paymentId})">Lihat Bukti</button>`;
                        } else {
                            paymentActionBtn = `<button class="btn-outline" onclick="openUploadFormFor(${paymentId})">Bayar / Bukti</button>`;
                        }
                    } else {
                        // no payment row yet: offer to choose payment method via modal
                        paymentActionBtn = `<button class="btn-primary" onclick="(function(){ window.currentOrderId = ${order.id}; openPaymentModal(); })()">Pilih Metode</button>`;
                    }

                    return `
                    <tr>
                        <td>#${order.id}</td>
                        <td>${order.jenis_jasa}</td>
                        <td>${formatDate(order.tanggal_pemesanan)}</td>
                        <td>${formatDate(order.tanggal_jadwal)} ${order.waktu_jadwal || ''}</td>
                        <td><span class="status-badge ${getStatusClass(order.status_pemesanan)}">${order.status_pemesanan}</span></td>
                        <td>${order.teknisi_nama || 'Belum ditugaskan'}</td>
                        <td>
                            <button class="btn-outline" onclick="viewOrderDetail(${order.id})">Detail</button>
                            ${paymentActionBtn}
                        </td>
                    </tr>
                `;
                }).join('');
            } else {
                tbody.innerHTML = '<tr><td colspan="7" class="no-data">Belum ada pesanan</td></tr>';
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">Gagal memuat data pesanan</td></tr>';
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        document.getElementById('orders-tbody').innerHTML = '<tr><td colspan="7" class="no-data">Terjadi kesalahan saat memuat data</td></tr>';
    }
}

// Load payments history
async function loadPaymentsHistory() {
    try {
        const response = await NetFastAuth.apiCall('/user/payments/');
        const tbody = document.getElementById('payments-tbody');
        
        if (response && response.ok) {
            const data = await response.json();
            console.log('loadPaymentsHistory:', data);
            
            if (data.payments && data.payments.length > 0) {
                tbody.innerHTML = data.payments.map(payment => {
                    const status = (payment.status_pembayaran || '').toLowerCase();
                    let actionBtn = `<button class="btn-outline" onclick="downloadInvoice(${payment.id})">Invoice</button>`;
                    if (status.includes('menunggu') || status.includes('belum') || status.includes('pending')) {
                        actionBtn = `<button class="btn-primary" onclick="openUploadFormFor(${payment.id})">Unggah Bukti</button>`;
                    } else if (status.includes('verifikasi') || status.includes('menunggu verifikasi')) {
                        actionBtn = `<button class="btn-outline" onclick="openUploadFormFor(${payment.id})">Lihat Bukti</button>`;
                    }

                    return `
                    <tr>
                        <td>#${payment.id}</td>
                        <td>${formatDate(payment.tanggal_pembayaran)}</td>
                        <td>${formatCurrency(payment.jumlah)}</td>
                        <td>${payment.metode_pembayaran}</td>
                        <td><span class="status-badge ${getStatusClass(payment.status_pembayaran)}">${payment.status_pembayaran}</span></td>
                        <td>${payment.periode_tagihan}</td>
                        <td>
                            ${actionBtn}
                        </td>
                    </tr>
                `;
                }).join('');
            } else {
                tbody.innerHTML = '<tr><td colspan="7" class="no-data">Belum ada riwayat pembayaran</td></tr>';
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="7" class="no-data">Gagal memuat data pembayaran</td></tr>';
        }
    } catch (error) {
        console.error('Error loading payments:', error);
        document.getElementById('payments-tbody').innerHTML = '<tr><td colspan="7" class="no-data">Terjadi kesalahan saat memuat data</td></tr>';
    }
}

// Load order detail for modal
async function loadOrderDetail(orderId) {
    try {
        const response = await NetFastAuth.apiCall(`/orders/${orderId}/`);
        
        if (response && response.ok) {
            const order = await response.json();
            
            document.getElementById('order-detail-content').innerHTML = `
                <div class="order-detail">
                    <h4>Pesanan #${order.id}</h4>
                    <div class="detail-grid">
                        <div><strong>Jenis Jasa:</strong> ${order.jenis_jasa}</div>
                        <div><strong>Status:</strong> <span class="status-badge ${getStatusClass(order.status_pemesanan)}">${order.status_pemesanan}</span></div>
                        <div><strong>Tanggal Pesanan:</strong> ${formatDate(order.tanggal_pesanan)}</div>
                        <div><strong>Jadwal Layanan:</strong> ${formatDate(order.tanggal_jadwal)} ${order.waktu_jadwal || ''}</div>

                        <div><strong>Teknisi:</strong> ${order.teknisi_nama || 'Belum ditugaskan'}</div>
                        <div><strong>Kontak Darurat:</strong> ${order.kontak_darurat || '-'}</div>
                        <div><strong>Catatan:</strong> ${order.catatan || 'Tidak ada catatan'}</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading order detail:', error);
        NetFastAuth.showAlert('Gagal memuat detail pesanan', 'error');
    }
}

// Utility functions
function formatCurrency(amount) {
    if (!amount) return 'Rp 0';
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getStatusClass(status) {
    const statusMap = {
        'Aktif': 'active',
        'Lunas': 'active',
        'Selesai': 'active',
        'Tidak Aktif': 'inactive',
        'Belum Bayar': 'pending',
        'Menunggu Penugasan': 'pending',
        'Ditugaskan': 'pending',
        'Dalam Proses': 'pending',
        'Dibatalkan': 'inactive'
    };
    return statusMap[status] || 'pending';
}

function downloadInvoice(paymentId) {
    // This would typically download a PDF invoice
    NetFastAuth.showAlert('Fitur download invoice akan segera tersedia', 'info');
}

// Export functions for global use
window.NetFastUser = {
    loadUserName,
    loadDashboardData,
    loadJenisJasa,
    loadOrdersHistory,
    loadPaymentsHistory,
    loadOrderDetail
};
