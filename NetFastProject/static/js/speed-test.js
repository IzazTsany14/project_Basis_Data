// NetFast - Speed Test Logic
let isTestRunning = false;
let testResults = null;

// Start speed test simulation
async function startSpeedTest() {
    if (isTestRunning) return;
    
    isTestRunning = true;
    const startBtn = document.getElementById('start-test-btn');
    const progressDiv = document.getElementById('test-progress');
    const resultsDiv = document.getElementById('test-results');
    
    // Hide results and show progress
    resultsDiv.classList.add('hidden');
    progressDiv.classList.remove('hidden');
    startBtn.disabled = true;
    
    try {
        // Simulate download test
        await runTestPhase('Download', 'Mengukur kecepatan download...', 3000);
        
        // Simulate upload test
        await runTestPhase('Upload', 'Mengukur kecepatan upload...', 2500);
        
        // Simulate ping test
        await runTestPhase('Ping', 'Mengukur latency...', 1500);
        
        // Generate and display results
        generateTestResults();
        showTestResults();
        
    } catch (error) {
        console.error('Speed test error:', error);
        NetFastAuth.showAlert('Terjadi kesalahan saat melakukan tes kecepatan', 'error');
    } finally {
        isTestRunning = false;
        startBtn.disabled = false;
        progressDiv.classList.add('hidden');
    }
}

// Simulate test phase with progress
function runTestPhase(phase, message, duration) {
    return new Promise((resolve) => {
        const progressText = document.getElementById('progress-text');
        const progressFill = document.getElementById('progress-fill');
        
        progressText.textContent = message;
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            progressFill.style.width = `${Math.min(progress, 100)}%`;
            
            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(resolve, 200);
            }
        }, duration / 50);
    });
}

// Generate realistic test results
function generateTestResults() {
    // Generate realistic speeds based on common internet packages in Indonesia
    const downloadSpeeds = [10, 15, 20, 25, 30, 50, 75, 100]; // Mbps
    const baseDownload = downloadSpeeds[Math.floor(Math.random() * downloadSpeeds.length)];
    
    // Upload is typically 10-50% of download speed
    const uploadRatio = 0.1 + (Math.random() * 0.4);
    const baseUpload = Math.round(baseDownload * uploadRatio);
    
    // Add some variance (±20%)
    const downloadVariance = 0.8 + (Math.random() * 0.4);
    const uploadVariance = 0.8 + (Math.random() * 0.4);
    
    const downloadSpeed = Math.round(baseDownload * downloadVariance * 10) / 10;
    const uploadSpeed = Math.round(baseUpload * uploadVariance * 10) / 10;
    
    // Ping: typically 10-100ms for Indonesian connections
    const basePing = 15 + (Math.random() * 60);
    const ping = Math.round(basePing);
    
    testResults = {
        download: downloadSpeed,
        upload: uploadSpeed,
        ping: ping,
        timestamp: new Date().toISOString()
    };
}

// Display test results
function showTestResults() {
    const resultsDiv = document.getElementById('test-results');
    
    // Animate the results display
    document.getElementById('download-speed').textContent = `${testResults.download} Mbps`;
    document.getElementById('upload-speed').textContent = `${testResults.upload} Mbps`;
    document.getElementById('ping-value').textContent = `${testResults.ping} ms`;
    
    resultsDiv.classList.remove('hidden');
    
    // Animate numbers counting up
    animateNumber('download-speed', 0, testResults.download, 'Mbps', 1500);
    animateNumber('upload-speed', 0, testResults.upload, 'Mbps', 1500);
    animateNumber('ping-value', 0, testResults.ping, 'ms', 1500);
}

// Animate number counting
function animateNumber(elementId, start, end, unit, duration) {
    const element = document.getElementById(elementId);
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * easeOut;
        
        element.textContent = `${current.toFixed(1)} ${unit}`;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        } else {
            element.textContent = `${end} ${unit}`;
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Save test results to API
async function saveTestResult() {
    if (!testResults) {
        NetFastAuth.showAlert('Tidak ada hasil tes untuk disimpan', 'error');
        return;
    }
    
    const saveBtn = document.getElementById('save-result-btn');
    
    try {
        NetFastAuth.showLoading(saveBtn);
        
        const testData = {
            id_pelanggan: localStorage.getItem('userId'),
            kecepatan_download: testResults.download,
            kecepatan_upload: testResults.upload,
            ping: testResults.ping,
            tanggal_testing: testResults.timestamp,
            lokasi_testing: 'Web Dashboard' // Could be enhanced to get actual location
        };
        
        const response = await NetFastAuth.apiCall('/speed-test/', {
            method: 'POST',
            body: JSON.stringify(testData)
        });
        
        if (response && response.ok) {
            NetFastAuth.showAlert('Hasil tes berhasil disimpan!', 'success');
            
            // Refresh test history
            setTimeout(() => {
                loadTestHistory();
            }, 1000);
            
            // Disable save button
            saveBtn.disabled = true;
            saveBtn.textContent = '✓ Tersimpan';
        } else {
            const error = await response.json();
            NetFastAuth.showAlert(error.message || 'Gagal menyimpan hasil tes', 'error');
        }
    } catch (error) {
        console.error('Error saving test result:', error);
        NetFastAuth.showAlert('Terjadi kesalahan saat menyimpan hasil', 'error');
    } finally {
        NetFastAuth.hideLoading(saveBtn);
    }
}

// Reset test interface
function resetTest() {
    testResults = null;
    
    // Reset UI elements
    document.getElementById('test-results').classList.add('hidden');
    document.getElementById('test-progress').classList.add('hidden');
    document.getElementById('progress-fill').style.width = '0%';
    
    const saveBtn = document.getElementById('save-result-btn');
    saveBtn.disabled = false;
    saveBtn.textContent = '💾 Simpan Hasil';
    
    const startBtn = document.getElementById('start-test-btn');
    startBtn.disabled = false;
}

// Load test history
async function loadTestHistory() {
    try {
        const response = await NetFastAuth.apiCall('/user/speed-test-history/');
        const historyContainer = document.getElementById('test-history');
        
        if (response && response.ok) {
            const data = await response.json();
            
            if (data.tests && data.tests.length > 0) {
                // Show last 5 tests
                const recentTests = data.tests.slice(0, 5);
                
                historyContainer.innerHTML = `
                    <div class="history-list">
                        ${recentTests.map(test => `
                            <div class="history-item">
                                <div class="history-date">${formatDate(test.tanggal_testing)}</div>
                                <div class="history-speeds">
                                    <span>⬇️ ${test.kecepatan_download} Mbps</span>
                                    <span>⬆️ ${test.kecepatan_upload} Mbps</span>
                                    <span>📡 ${test.ping} ms</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="history-footer">
                        <a href="riwayat-pesanan.html" class="btn-outline">Lihat Semua Riwayat</a>
                    </div>
                `;
            } else {
                historyContainer.innerHTML = '<p>Belum ada riwayat tes</p>';
            }
        } else {
            // Show sample data if API fails
            showSampleTestHistory();
        }
    } catch (error) {
        console.error('Error loading test history:', error);
        showSampleTestHistory();
    }
}

// Show sample test history for demo
function showSampleTestHistory() {
    const historyContainer = document.getElementById('test-history');
    const sampleTests = [
        { date: new Date(Date.now() - 86400000), download: 25.3, upload: 5.2, ping: 28 },
        { date: new Date(Date.now() - 172800000), download: 23.8, upload: 4.9, ping: 32 },
        { date: new Date(Date.now() - 259200000), download: 26.1, upload: 5.5, ping: 25 }
    ];
    
    historyContainer.innerHTML = `
        <div class="history-list">
            ${sampleTests.map(test => `
                <div class="history-item">
                    <div class="history-date">${formatDate(test.date.toISOString())}</div>
                    <div class="history-speeds">
                        <span>⬇️ ${test.download} Mbps</span>
                        <span>⬆️ ${test.upload} Mbps</span>
                        <span>📡 ${test.ping} ms</span>
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="history-footer">
            <small style="color: var(--text-light);">Data contoh - Hubungkan ke API untuk data real</small>
        </div>
    `;
}

// Utility function for date formatting
function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Add CSS for history items
const historyStyles = `
    .history-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .history-item {
        padding: 0.75rem;
        background: var(--light-bg);
        border-radius: 6px;
        border-left: 3px solid var(--primary-color);
    }
    
    .history-date {
        font-size: 12px;
        color: var(--text-light);
        margin-bottom: 0.25rem;
    }
    
    .history-speeds {
        display: flex;
        gap: 1rem;
        font-size: 14px;
        font-weight: 500;
    }
    
    .history-speeds span {
        color: var(--text-dark);
    }
    
    .history-footer {
        margin-top: 1rem;
        text-align: center;
    }
    
    @media (max-width: 768px) {
        .history-speeds {
            flex-direction: column;
            gap: 0.25rem;
        }
    }
`;

// Inject styles
if (!document.getElementById('speed-test-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'speed-test-styles';
    styleSheet.textContent = historyStyles;
    document.head.appendChild(styleSheet);
}

// Export functions for global use
window.NetFastSpeedTest = {
    startSpeedTest,
    saveTestResult,
    resetTest,
    loadTestHistory
};
