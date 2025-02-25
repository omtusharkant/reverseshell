document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    socket.on('client_count', (data) => {
        document.getElementById('clientCount').textContent = data.count;
    });
});

function generateApi() {
    const username = document.getElementById('usernameInput').value;
    fetch('/generate_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('apikey').textContent = data.apikey;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function verifyApiKey() {
    const apiKey = document.getElementById('apiKeyInput').value;
    fetch('/verify_api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'API-Key': apiKey
        }
    })
    .then(response => {
        if (response.ok) {
            alert('API Key is valid');
        } else {
            alert('API Key is invalid');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function sendCommand() {
    const command = document.getElementById('commandInput').value;
    
    fetch('/set_command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => response.json())
    .then(data => {
        const outputElement = document.getElementById('output');
        outputElement.textContent = data.status;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}