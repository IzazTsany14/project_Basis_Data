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

    if (path.includes('dashboard.html')) {
        loadTugasTeknisi();
    }

    if (path.includes('detail-tugas.html')) {
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
        const response = await fetch('/teknisi/tugas/');
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
            row.innerHTML = `
                <td>${task.id_pemesanan}</td>
                <td>${task.nama_jasa}</td>
                <td>${task.nama_pelanggan}</td>
                <td>${task.alamat_pemasangan}</td>
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
            const result = await fetchWithAuth(`${API_BASE_URL}/teknisi/tugas/status-update/`, {
                method: 'PUT',
                body: JSON.stringify({
                    id_pemesanan: idPesanan,
                    status_pemesanan: newStatus,
                }),
            });
            alert('Status berhasil diperbarui!');
            console.log(result);
            window.location.href = 'dashboard.html'; // Redirect after update
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
