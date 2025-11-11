// Base URL for the API. Adjust if your API is hosted elsewhere.
const API_BASE_URL = '/api';

// Function to get the authentication token (implement as needed)
function getAuthToken() {
    // This is a placeholder. Replace with your actual token retrieval logic,
    // e.g., from localStorage, cookies, etc.
    return localStorage.getItem('authToken');
}

// Helper function for authenticated API requests
async function fetchWithAuth(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`,
        ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    // For DELETE requests, there might not be a JSON body
    if (options.method === 'DELETE' && response.status === 204) {
        return;
    }
    return response.json();
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if (path.includes('dashboard.html')) {
        loadAdminDashboardStats();
    } else if (path.includes('manajemen-pesanan.html')) {
        loadPesananBaru();
        loadPesananDikerjakan();
    } else if (path.includes('manajemen-teknisi.html')) {
        loadTeknisiList();
        setupTeknisiForm();
    } else if (path.includes('manajemen-pelanggan.html')) {
        loadPelangganList();
        setupPelangganForm();
    }
});

async function loadAdminDashboardStats() {
    try {
        // Assumes an endpoint that returns summary statistics
        const response = await fetch('/admin/dashboard/stats/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const stats = await response.json();
        document.getElementById('stat-pelanggan-aktif').textContent = stats.total_pelanggan || 0;
        document.getElementById('stat-pesanan-baru').textContent = stats.pemesanan_menunggu || 0;
        document.getElementById('stat-teknisi-tersedia').textContent = stats.total_teknisi || 0;
    } catch (error) {
        console.error('Failed to load admin stats:', error);
    }
}

// --- Manajemen Pesanan ---
async function loadPesananBaru() {
    const pesananBaruList = document.getElementById('pesanan-baru-list');
    if (!pesananBaruList) return;

    try {
        const [pesanan, teknisi] = await Promise.all([
            fetchWithAuth(`${API_BASE_URL}/admin/pesanan/?status=Menunggu Penugasan`),
            fetchWithAuth(`${API_BASE_URL}/admin/teknisi/`)
        ]);

        const teknisiOptions = teknisi.map(t => `<option value="${t.id_teknisi}">${t.nama}</option>`).join('');

        pesananBaruList.innerHTML = '';
        pesanan.forEach(p => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${p.id_pemesanan}</td>
                <td>${p.nama_pelanggan}</td>
                <td>${p.alamat_pemasangan}</td>
                <td>${p.jenis_jasa}</td>
                <td>
                    <select id="teknisi-for-${p.id_pemesanan}">
                        <option value="">Pilih Teknisi</option>
                        ${teknisiOptions}
                    </select>
                </td>
                <td>
                    <button onclick="assignTeknisi(${p.id_pemesanan})">Tugaskan</button>
                </td>
            `;
            pesananBaruList.appendChild(row);
        });
    } catch (error) {
        console.error('Failed to load new orders:', error);
        pesananBaruList.innerHTML = `<tr><td colspan="6">Gagal memuat data.</td></tr>`;
    }
}

async function loadPesananDikerjakan() {
    // Similar to loadPesananBaru, but for ongoing tasks
}

async function assignTeknisi(id_pemesanan) {
    const teknisiSelect = document.getElementById(`teknisi-for-${id_pemesanan}`);
    const id_teknisi = teknisiSelect.value;

    if (!id_teknisi) {
        alert('Silakan pilih teknisi terlebih dahulu.');
        return;
    }

    try {
        await fetchWithAuth(`${API_BASE_URL}/admin/penugasan-update/`, {
            method: 'PUT',
            body: JSON.stringify({ id_pemesanan, id_teknisi })
        });
        alert('Teknisi berhasil ditugaskan!');
        loadPesananBaru(); // Refresh the list
    } catch (error) {
        console.error('Failed to assign technician:', error);
        alert(`Gagal menugaskan teknisi: ${error.message}`);
    }
}

// --- Manajemen Teknisi (CRUD) ---
async function loadTeknisiList() {
    const tableBody = document.getElementById('teknisi-table-body');
    if (!tableBody) return;
    try {
        const teknisiList = await fetchWithAuth(`${API_BASE_URL}/admin/teknisi/`);
        tableBody.innerHTML = '';
        teknisiList.forEach(t => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${t.id_teknisi}</td>
                <td>${t.nama}</td>
                <td>${t.username}</td>
                <td>${t.nama_area}</td>
                <td>
                    <button onclick="editTeknisi(${t.id_teknisi})">Edit</button>
                    <button onclick="deleteTeknisi(${t.id_teknisi})">Hapus</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Failed to load technicians:', error);
    }
}

function setupTeknisiForm() {
    const form = document.getElementById('form-manajemen-teknisi');
    if (!form) return;

    // Populate area layanan dropdown
    fetchWithAuth(`${API_BASE_URL}/admin/area-layanan/`).then(areas => {
        const select = document.getElementById('area-layanan-teknisi');
        select.innerHTML = areas.map(a => `<option value="${a.id_area}">${a.nama_area}</option>`).join('');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const method = data.id_teknisi ? 'PUT' : 'POST';
        const url = data.id_teknisi ? `${API_BASE_URL}/admin/teknisi/${data.id_teknisi}/` : `${API_BASE_URL}/admin/teknisi/`;

        // Remove password if it's empty during an update
        if (method === 'PUT' && !data.password) {
            delete data.password;
        }

        try {
            await fetchWithAuth(url, { method, body: JSON.stringify(data) });
            alert(`Teknisi berhasil ${method === 'POST' ? 'dibuat' : 'diperbarui'}!`);
            form.reset();
            loadTeknisiList();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });
}

async function editTeknisi(id) {
    // Fetch technician data and populate the form
}

async function deleteTeknisi(id) {
    if (!confirm('Apakah Anda yakin ingin menghapus teknisi ini?')) return;
    try {
        await fetchWithAuth(`${API_BASE_URL}/admin/teknisi/${id}/`, { method: 'DELETE' });
        alert('Teknisi berhasil dihapus.');
        loadTeknisiList();
    } catch (error) {
        alert(`Gagal menghapus: ${error.message}`);
    }
}

// --- Manajemen Pelanggan (Placeholder) ---
function loadPelangganList() {
    console.log('Loading customer list...');
}

function setupPelangganForm() {
    console.log('Setting up customer form...');
}
