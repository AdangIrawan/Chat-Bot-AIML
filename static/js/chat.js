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
        chatbox.innerHTML += '<div class="message user">' + input + '</div>';

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = xhr.responseText;
                chatbox.innerHTML += '<div class="message bot">' + response + '</div>';
                chatbox.scrollTop = chatbox.scrollHeight;
                sessionStorage.setItem('chatHistory', chatbox.innerHTML);
            }
        };
        xhr.open("POST", "/get_response", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("user_input=" + input);

        document.getElementById('pertanyaan').value = '';
    });
});
