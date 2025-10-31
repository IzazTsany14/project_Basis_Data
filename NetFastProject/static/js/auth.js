// NetFast - Authentication Logic
document.addEventListener('DOMContentLoaded', function() {
    // Helper: get CSRF token from cookie if no hidden input is present
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrftokenInput ? csrftokenInput.value : getCookie('csrftoken');

    // Support both ID variants used in templates to avoid mismatch
    const customerLoginForm = document.getElementById('login-pelanggan-form') || document.getElementById('loginPelangganForm') || document.getElementById('loginPelangganForm') || document.getElementById('loginPelangganForm');
    if (customerLoginForm) {
        customerLoginForm.addEventListener('submit', handleCustomerLogin);
    }

    const staffLoginForm = document.getElementById('login-staf-form') || document.getElementById('loginStafForm') || document.getElementById('loginStafForm');
    if (staffLoginForm) {
        staffLoginForm.addEventListener('submit', handleStaffLogin);
    }

    const registerForm = document.getElementById('register-form') || document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }

    // Expose csrftoken to handlers via closure
    window.__NETFAST_CSRF = csrftoken;
});

// Handle customer login
async function handleCustomerLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    try {
        showLoading(event.target.querySelector('button[type="submit"]'));
        
        const response = await fetch('/auth/login/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': window.__NETFAST_CSRF || '',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: formData.get('email'),
                password: formData.get('password')
            })
        });

        const result = await response.json();

        if (response.ok) {
            // Backend returns { message, user }
            const user = result.user || {};
            // Save minimal info locally to control SPA behavior
            localStorage.setItem('userId', user.id || user.id_pelanggan || '');
            localStorage.setItem('userRole', 'PELANGGAN');
            localStorage.setItem('userName', user.nama || user.nama_lengkap || '');

            showAlert('Login berhasil! Mengalihkan ke dashboard...', 'success');
            // Redirect to canonical dashboard URL
            setTimeout(() => {
                window.location.href = '/user/dashboard/';
            }, 800);
        } else {
            showAlert(result.error || result.message || 'Login gagal. Periksa email dan password Anda.', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Terjadi kesalahan koneksi. Silakan coba lagi.', 'error');
    } finally {
        hideLoading(event.target.querySelector('button[type="submit"]'));
    }
}

// Handle staff login
async function handleStaffLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        email: formData.get('email'),
        password: formData.get('password'),
        user_type: formData.get('role')
    };

    try {
        showLoading(event.target.querySelector('button[type="submit"]'));
        
        // Staff login should call same backend endpoint; include credentials
        const response = await fetch('/auth/login/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': window.__NETFAST_CSRF || '',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login_id: formData.get('email') || formData.get('username'), password: formData.get('password') })
        });

        const result = await response.json();

        if (response.ok) {
            const user = result.user || {};
            localStorage.setItem('userId', user.id || user.id_teknisi || '');
            localStorage.setItem('userRole', user.role_akses || loginData.user_type || 'TEKNISI');
            localStorage.setItem('userName', user.nama || user.nama_teknisi || '');

            showAlert('Login berhasil! Mengalihkan ke dashboard...', 'success');
            setTimeout(() => {
                if ((user.role_akses || loginData.user_type || '').toUpperCase() === 'ADMIN') {
                    window.location.href = '/admin/dashboard/';
                } else {
                    window.location.href = '/teknisi/dashboard/';
                }
            }, 800);
        } else {
            showAlert(result.error || result.message || 'Login gagal. Periksa kredensial Anda.', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Terjadi kesalahan koneksi. Silakan coba lagi.', 'error');
    } finally {
        hideLoading(event.target.querySelector('button[type="submit"]'));
    }
}

// Handle customer registration
async function handleRegistration(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    // Validate password confirmation
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm-password');
    
    if (password !== confirmPassword) {
        showAlert('Password dan konfirmasi password tidak cocok.', 'error');
        return;
    }

    const registrationData = {
        nama: formData.get('nama'),
        email: formData.get('email'),
        password: password,
        alamat: formData.get('alamat'),
        telepon: formData.get('telepon'),
        tanggal_lahir: formData.get('tanggal_lahir') || null
    };

    try {
        showLoading(event.target.querySelector('button[type="submit"]'));
        
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData)
        });

        const result = await response.json();

        if (response.ok) {
            showAlert('Registrasi berhasil! Silakan login dengan akun Anda.', 'success');
            
            // Redirect to login page
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            const errorMessage = result.message || 'Registrasi gagal. Silakan periksa data Anda.';
            showAlert(errorMessage, 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert('Terjadi kesalahan koneksi. Silakan coba lagi.', 'error');
    } finally {
        hideLoading(event.target.querySelector('button[type="submit"]'));
    }
}

// Check authentication status
function checkAuthStatus() {
    const token = localStorage.getItem('userToken');
    const userRole = localStorage.getItem('userRole');
    
    // If on login/register page and user is already logged in, redirect
    if (token && (window.location.pathname.includes('index.html') || window.location.pathname.includes('register.html') || window.location.pathname === '/')) {
        if (userRole === 'PELANGGAN') {
            window.location.href = 'user/dashboard.html';
        } else if (userRole === 'ADMIN') {
            window.location.href = 'admin/dashboard.html';
        } else if (userRole === 'TEKNISI') {
            window.location.href = 'teknisi/dashboard.html';
        }
    }
    
    // If on protected page and no token, redirect to login
    if (!token && (window.location.pathname.includes('dashboard.html') || 
                   window.location.pathname.includes('user/') || 
                   window.location.pathname.includes('admin/') || 
                   window.location.pathname.includes('teknisi/'))) {
        window.location.href = '../index.html';
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // Insert alert at the top of the form or container
    const container = document.querySelector('.login-form.active') || 
                     document.querySelector('.register-form') || 
                     document.querySelector('.card-body') ||
                     document.body;
    
    container.insertBefore(alert, container.firstChild);
    
    // Auto remove alert after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function showLoading(button) {
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Memproses...';
}

function hideLoading(button) {
    button.disabled = false;
    // Restore original button text based on context
    if (button.closest('#login-pelanggan-form')) {
        button.textContent = 'Login';
    } else if (button.closest('#login-staf-form')) {
        button.textContent = 'Login';
    } else if (button.closest('#register-form')) {
        button.textContent = 'Daftar Sekarang';
    }
}

// API helper function
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('userToken');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);
        
        // Handle unauthorized access
        if (response.status === 401) {
            localStorage.clear();
            window.location.href = '../index.html';
            return;
        }
        
        return response;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Export for use in other files
window.NetFastAuth = {
    apiCall,
    showAlert,
    showLoading,
    hideLoading,
    checkAuthStatus
};