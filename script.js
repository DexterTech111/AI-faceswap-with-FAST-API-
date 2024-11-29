// script.js

// Base URL of your API
const API_BASE_URL = "http://localhost:8000"; // Update if necessary

// Function to create a new user
document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const isAdmin = document.getElementById('isAdmin').checked;

    try {
        const response = await fetch(`${API_BASE_URL}/users?is_admin=${isAdmin}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('createUserResponse').innerHTML = `
                <div class="alert alert-success" role="alert">
                    User created successfully!<br>
                    <strong>API Key:</strong> ${data.api_key}<br>
                    <strong>API Token:</strong> ${data.api_token}
                </div>
            `;
        } else {
            document.getElementById('createUserResponse').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Error: ${data.detail}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to get all users
document.getElementById('getUsersForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const apiKey = document.getElementById('apiKey').value;
    const apiToken = document.getElementById('apiToken').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'api_key': apiKey,
                'api_token': apiToken
            }
        });

        const data = await response.json();

        if (response.ok) {
            let usersList = '<ul class="list-group">';
            data.forEach(user => {
                usersList += `<li class="list-group-item">
                    <strong>Username:</strong> ${user.username}<br>
                    <strong>Balance:</strong> ${user.balance}<br>
                    <strong>Active:</strong> ${user.is_active}<br>
                    <strong>Admin:</strong> ${user.is_admin}
                </li>`;
            });
            usersList += '</ul>';

            document.getElementById('getUsersResponse').innerHTML = usersList;
        } else {
            document.getElementById('getUsersResponse').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Error: ${data.detail}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to perform face swap
document.getElementById('faceSwapForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const { apiKey, apiToken } = getApiCredentials();

    if (!apiKey || !apiToken) {
        alert('Please set your API credentials first.');
        return;
    }

    const selfieId = document.getElementById('selfieId').value;
    const targetImageFile = document.getElementById('targetImageFile').files[0];

    const formData = new FormData();
    formData.append('selfie_id', selfieId);
    formData.append('target_image', targetImageFile);

    try {
        const response = await fetch(`${API_BASE_URL}/faceswap`, {
            method: 'POST',
            headers: {
                'api_key': apiKey,
                'api_token': apiToken
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('faceSwapResponse').innerHTML = `
                <div class="alert alert-success" role="alert">
                    Face swap successful!
                </div>
                <img src="${API_BASE_URL}/${data.swapped_image_url}" class="img-fluid" alt="Swapped Image">
            `;
        } else {
            document.getElementById('faceSwapResponse').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Error: ${data.detail}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

