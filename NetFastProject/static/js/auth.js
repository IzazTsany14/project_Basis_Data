// NetFast - Authentication Logic
const API_BASE_URL = 'http://localhost:8000/api'; // Adjust this to your Django API URL

// Login functionality for customers
document.addEventListener('DOMContentLoaded', function() {
    // Customer login form
    const customerLoginForm = document.getElementById('login-pelanggan-form');
    if (customerLoginForm) {
        customerLoginForm.addEventListener('submit', handleCustomerLogin);
    }

    // Staff login form
    const staffLoginForm = document.getElementById('login-staf-form');
    if (staffLoginForm) {
        staffLoginForm.addEventListener('submit', handleStaffLogin);
    }

    // Registration form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }

    // Check if user is already logged in
    checkAuthStatus();
});

// Handle customer login
async function handleCustomerLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        email: formData.get('email'),
        password: formData.get('password'),
        user_type: 'PELANGGAN'
    };

    try {
        showLoading(event.target.querySelector('button[type="submit"]'));
        
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        if (response.ok) {
            // Store user data in localStorage
            localStorage.setItem('userToken', result.token || result.access_token);
            localStorage.setItem('userId', result.user.id);
            localStorage.setItem('userRole', 'PELANGGAN');
            localStorage.setItem('userName', result.user.nama);

            showAlert('Login berhasil! Mengalihkan ke dashboard...', 'success');
            
            // Redirect to user dashboard
            setTimeout(() => {
                window.location.href = 'user/dashboard.html';
            }, 1500);
        } else {
            showAlert(result.message || 'Login gagal. Periksa email dan password Anda.', 'error');
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
        
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        if (response.ok) {
            // Store user data in localStorage
            localStorage.setItem('userToken', result.token || result.access_token);
            localStorage.setItem('userId', result.user.id);
            localStorage.setItem('userRole', loginData.user_type);
            localStorage.setItem('userName', result.user.nama);

            showAlert('Login berhasil! Mengalihkan ke dashboard...', 'success');
            
            // Redirect based on role
            setTimeout(() => {
                if (loginData.user_type === 'ADMIN') {
                    window.location.href = 'admin/dashboard.html';
                } else if (loginData.user_type === 'TEKNISI') {
                    window.location.href = 'teknisi/dashboard.html';
                }
            }, 1500);
        } else {
            showAlert(result.message || 'Login gagal. Periksa kredensial Anda.', 'error');
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