document.addEventListener("DOMContentLoaded", function () {
    getUserInformation();

    // Add an event listener for the Enter key in the user input field
    document.getElementById('user-input').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});

function getUserInformation() {
    document.getElementById('chat-output').innerHTML = "<p>Welcome! Ask me anything or have a chat.</p>";
}

function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        document.getElementById('chat-output').innerHTML += "<p><strong>You:</strong> " + userInput + "</p>";
        showGeneratingResponse();
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/chat", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var formattedResponse = formatCode(response.bot_response);
                document.getElementById('chat-output').innerHTML += formattedResponse;
                hideGeneratingResponse();
            }
        };
        xhr.send("user_input=" + encodeURIComponent(userInput));
    }
    document.getElementById('user-input').value = "";
}

function showGeneratingResponse() {
    document.getElementById('generating-response').classList.remove('hidden');
}

function hideGeneratingResponse() {
    document.getElementById('generating-response').classList.add('hidden');
}

function formatCode(text) {
    var codeRegex = /```([\s\S]+?)```/g;
    var formattedText = text.replace(codeRegex, function (match, codeContent) {
        return '<pre class="code-snippet">' + codeContent + '<button class="copy-button" onclick="copyCode(this)">Copy</button></pre>';
    });
    return formattedText;
}

function copyCode(button) {
    var codeBlock = button.parentElement;
    var codeContent = codeBlock.textContent;
    var tempTextarea = document.createElement('textarea');
    tempTextarea.value = codeContent.trim();
    document.body.appendChild(tempTextarea);
    tempTextarea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextarea);
    button.textContent = 'Copied!';
    setTimeout(function () {
        button.textContent = 'Copy';
    }, 2000);
}
