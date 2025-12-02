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
    return response.json();
}


document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    // Check actual routes without .html extension
    if (path.includes('/teknisi/dashboard')) {
        loadTugasTeknisi();
    }

    if (path.includes('/teknisi/detail-tugas')) {
        displayTugasDetail();
        setupUpdateStatusForm();
        setupCatatPerangkatForm();
    }
});

/**
 * Fetches and displays the list of tasks for the logged-in technician.
 * GET /api/teknisi/tugas/
 */
async function loadTugasTeknisi() {
    const tugasListBody = document.getElementById('tugas-teknisi-list');
    if (!tugasListBody) return;

    try {
        // The backend now gets the technician ID from the session
        const response = await fetch('/api/teknisi/tugas/', {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        const tasks = await response.json();
        
        tugasListBody.innerHTML = ''; // Clear existing rows
        if (tasks.length === 0) {
            tugasListBody.innerHTML = `<tr><td colspan="6">Tidak ada tugas yang ditugaskan saat ini.</td></tr>`;
            return;
        }

        tasks.forEach(task => {
            const row = document.createElement('tr');
            // Ambil nama pelanggan dari relasi
            let namaPelanggan = '-';
            if (task.id_pelanggan && task.id_pelanggan.nama_lengkap) {
                namaPelanggan = task.id_pelanggan.nama_lengkap;
            }
            row.innerHTML = `
                <td>${task.id_pemesanan}</td>
                <td>${task.nama_jasa}</td>
                <td>${namaPelanggan}</td>
                <td>${task.alamat_pemasangan}</td>
                <td>${task.tanggal_pemesanan ? new Date(task.tanggal_pemesanan).toLocaleDateString('id-ID') : '-'}</td>
                <td>${task.status_pemesanan}</td>
                <td>
                    <a href="/teknisi/detail-tugas/?id=${task.id_pemesanan}" class="btn-detail">Lihat Detail</a>
                </td>
            `;
            tugasListBody.appendChild(row);
        });
    } catch (error) {
        console.error('Failed to load technician tasks:', error);
        tugasListBody.innerHTML = `<tr><td colspan="6">Gagal memuat data. ${error.message}</td></tr>`;
    }
}

/**
 * Displays the details of a specific task on the detail page.
 */
function displayTugasDetail() {
    const params = new URLSearchParams(window.location.search);
    const taskId = params.get('id');
    if (!taskId) return;

    // Fetch the specific task details (assuming an endpoint exists)
    // This might require a new endpoint or be passed via session/localStorage
    // For now, we'll assume the data can be fetched or was stored
    console.log(`Displaying details for task ID: ${taskId}`);
    document.getElementById('id-pesanan').value = taskId;
    // You would typically fetch the full details here and populate the customer info
    // e.g., fetchWithAuth(`${API_BASE_URL}/teknisi/tugas/${taskId}/`).then(...)
}

/**
 * Sets up the form for updating the task status.
 * PUT /api/teknisi/tugas/status-update/
 */
function setupUpdateStatusForm() {
    const statusForm = document.getElementById('form-update-status');
    if (!statusForm) return;

    statusForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const idPesanan = document.getElementById('id-pesanan').value;
        const newStatus = document.getElementById('status-pemesanan').value;

        try {
            const response = await fetch(`/teknisi/pemesanan/${idPesanan}/update/`, {
                method: 'PUT',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status_pemesanan: newStatus })
            });
            
            if (!response.ok) {
                throw new Error('Gagal memperbarui status');
            }
            
            alert('Status berhasil diperbarui!');
            window.location.href = '/teknisi/dashboard/'; // Redirect to teknisi dashboard
        } catch (error) {
            console.error('Failed to update status:', error);
            alert(`Gagal memperbarui status: ${error.message}`);
        }
    });
}

/**
 * Sets up the form for recording installed equipment.
 * POST /api/teknisi/catat-perangkat/
 */
function setupCatatPerangkatForm() {
    const perangkatForm = document.getElementById('form-catat-perangkat');
    if (!perangkatForm) return;

    // You would also need to populate the device type dropdown
    // e.g., fetchWithAuth(`${API_BASE_URL}/perangkat/`).then(...)

    perangkatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(perangkatForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const result = await fetchWithAuth(`${API_BASE_URL}/teknisi/catat-perangkat/`, {
                method: 'POST',
                body: JSON.stringify(data),
            });
            alert('Perangkat berhasil dicatat!');
            console.log(result);
            perangkatForm.reset();
        } catch (error) {
            console.error('Failed to record device:', error);
            alert(`Gagal mencatat perangkat: ${error.message}`);
        }
    });
}
