document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById('chatForm');
    var chatbox = document.getElementById('chatbox');

    fetch('/get_chat_history')
        .then(response => response.json())
        .then(data => {
            if (data.chatHistory) {
                chatbox.innerHTML = data.chatHistory;
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var input = document.getElementById('pertanyaan').value;

        chatbox.innerHTML += '<div class="message user">' + input + '</div>';

        document.getElementById('chatbox').lastElementChild.scrollIntoView();

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = xhr.responseText;

                setTimeout(function () {
                    chatbox.innerHTML += '<div class="message bot">' + response + '</div>';
                    chatbox.scrollTop = chatbox.scrollHeight;

                    fetch('/save_chat_history', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ chatHistory: chatbox.innerHTML })
                    });

                    document.getElementById('chatbox').lastElementChild.scrollIntoView();
                }, 1500);
            }
        };
        xhr.open("POST", "/get_response", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("user_input=" + input);

        document.getElementById('pertanyaan').value = '';
    });
});
