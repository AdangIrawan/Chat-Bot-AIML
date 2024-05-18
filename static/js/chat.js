document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById('chatForm');
    var chatbox = document.getElementById('chatbox');

    // Memeriksa apakah ada riwayat obrolan yang tersimpan di session storage
    var chatHistory = sessionStorage.getItem('chatHistory');
    if (chatHistory) {
        chatbox.innerHTML = chatHistory;
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var input = document.getElementById('pertanyaan').value;
        chatbox.innerHTML += '<div class="message user">' + 
        '<div class="user-text">' + input + '</div>' +
        '</div>';

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = xhr.responseText;
                var botMessage = '<div class="message bot">' +
                                 '<img src="static/image/CHATBOT.png" alt="Bot Icon" class="bot-icon">' +
                                 '<div class="bot-text">' + response + '</div>' +
                                 '</div>';
                chatbox.innerHTML += botMessage;
                chatbox.scrollTop = chatbox.scrollHeight;
                sessionStorage.setItem('chatHistory', chatbox.innerHTML);
            }
        };
        xhr.open("POST", "/get_response", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("user_input=" + input);

        document.getElementById('pertanyaan').value = '';
        });
});