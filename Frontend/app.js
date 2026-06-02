// Configuration: Base target URL pointing to your running local Django server gateway
const BASE_URL = 'http://127.0.0.1:8000/api';

// 1. SECURE AUTHENTICATION CONTROLLER (LOGIN HANDLER)

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const usernameInput = document.getElementById('username').value;
        const passwordInput = document.getElementById('password').value;
        const errorDiv = document.getElementById('authErrorMessage');
        
        errorDiv.textContent = ''; // Clear previous error messages

        try {
            // DRF SimpleJWT token path
            const response = await fetch(`${BASE_URL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: usernameInput,
                    password: passwordInput
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Securely store tokens and session identifier locally in browser storage
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('refreshToken', data.refresh);
                localStorage.setItem('username', usernameInput);
                
                // Redirect straight to our dashboard deck
                window.location.href = 'index.html';
            } else {
                errorDiv.textContent = data.detail || 'Authentication failed. Please verify credentials.';
            }
        } catch (error) {
            console.error('Login Pipeline Error:', error);
            errorDiv.textContent = 'Unable to reach backend gateway server.';
        }
    });
}

// -------------------------------------------------------------
// 2. CORE ANALYTICS PIPELINE SUBMISSION (POST REQUEST)
// -------------------------------------------------------------
const predictionForm = document.getElementById('predictionForm');
if (predictionForm) {
    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Capture numeric values from form inputs
        const payload = {
            cgpa: parseFloat(document.getElementById('cgpa').value),
            attendance_percentage: parseFloat(document.getElementById('attendance').value),
            number_of_backlogs: parseInt(document.getElementById('backlogs').value),
            coding_rating: parseInt(document.getElementById('codingRating').value)
        };

        const displayDiv = document.getElementById('predictionDisplay');
        displayDiv.innerHTML = '<p class="loading">Processing evaluation vectors inside ML engine...</p>';

        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch(`${BASE_URL}/student/predict/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Passing secure JWT Bearer key
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                // Render custom dynamic layout cards showing classification outcome
                displayDiv.innerHTML = `
                    <div class="result-card">
                        <h4>Status: <span class="highlight">${data.prediction_result}</span></h4>
                        <div class="metric-bar-container">
                            <label>Confidence Metric:</label>
                            <div class="progress-bar" style="width: ${Math.min(data.probability_score, 100)}%"></div>
                            <span>${data.probability_score}%</span>
                        </div>
                    </div>
                `;
                // Auto-refresh historical logs data rows instantly!
                loadHistoryLogs();
            } else {
                displayDiv.innerHTML = `<p class="error-text">Execution Blocked: ${data.error || 'Validation error'}</p>`;
            }
        } catch (error) {
            console.error('Prediction Failure:', error);
            displayDiv.innerHTML = '<p class="error-text">API error. Pipeline interrupted.</p>';
        }
    });
}

// -------------------------------------------------------------
// 3. PERSISTENT HISTORY RETRIEVAL ENGINE (GET REQUEST)
// -------------------------------------------------------------
async function loadHistoryLogs() {
    const tableBody = document.getElementById('historyTableBody');
    const displayUserSpan = document.getElementById('displayUsername');
    
    if (!tableBody) return;

    // Display current student context string
    if (displayUserSpan) {
        displayUserSpan.textContent = `Student: ${localStorage.getItem('username') || 'Portal User'}`;
    }

    try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`${BASE_URL}/student/predictions/history/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            tableBody.innerHTML = ''; // Clear out loading text row placeholder

            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No predictive runs recorded yet.</td></tr>';
                return;
            }

            // Loop through log array state object context
            data.forEach(log => {
                const date = new Date(log.predicted_at).toLocaleString();
                const features = log.input_features;
                const featureString = `CGPA: ${features.cgpa} | Attd: ${features.attendance_percentage}% | Backlogs: ${features.number_of_backlogs} | Coding: ${features.coding_rating}/5`;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>#${log.id}</strong></td>
                    <td><small>${featureString}</small></td>
                    <td><span class="badge">${log.prediction_result}</span></td>
                    <td><strong>${log.probability_score}%</strong></td>
                    <td><span class="time-text">${date}</span></td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" class="error-text" style="text-align:center;">Failed to pull logs. Security access timeout.</td></tr>';
        }
    } catch (error) {
        console.error('History Query Failure:', error);
        tableBody.innerHTML = '<tr><td colspan="5" class="error-text" style="text-align:center;">Error fetching server data logs.</td></tr>';
    }
}

// -------------------------------------------------------------
// 4. SESSION DISCONNECT MANAGEMENT (LOGOUT TRIGGER)
// -------------------------------------------------------------
function logout() {
    localStorage.clear(); // Wipe the cache and security keys cleanly
    window.location.href = 'login.html';
}