async function sendMessage() {
    const userInput = document.getElementById('userInput').value.trim();
    if (userInput === "") return;

    appendMessage(userInput, 'user');
    document.getElementById('userInput').value = '';

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    if (data.reply) {
        appendMessage(data.reply, 'bot');
    } else {
        appendMessage("I'm sorry, I didn't understand that.", 'bot');
    }
}

function appendMessage(message, sender) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerText = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
