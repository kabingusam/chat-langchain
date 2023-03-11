var endpoint = "ws://localhost:9000/chat";
var ws = new WebSocket(endpoint);
// Receive message from server word by word. Display the words as they are received.
ws.onmessage = function (event) {
    var messages = document.getElementById('messages');
    var data = JSON.parse(event.data);
    if (data.sender === "bot") {
        if (data.type === "start") {
            var header = document.getElementById('header');
            header.innerHTML = "Computing answer...";
            var div = document.createElement('div');
            div.className = 'server-message';
            var p = document.createElement('p');
            p.innerHTML = "<strong>" + "Chatbot: " + "</strong>";
            div.appendChild(p);
            messages.appendChild(div);
        } else if (data.type === "stream") {
            var header = document.getElementById('header');
            header.innerHTML = "Chatbot is typing...";
            var p = messages.lastChild.lastChild;
            if (data.message === "\n") {
                p.innerHTML += "<br>";
            } else {
                p.innerHTML += data.message;
            }
        } else if (data.type === "info") {
            var header = document.getElementById('header');
            header.innerHTML = data.message;
        } else if (data.type === "end") {
            var header = document.getElementById('header');
            header.innerHTML = "Ask a question";
            var button = document.getElementById('send');
            button.innerHTML = "Send";
            button.disabled = false;
        } else if (data.type === "error") {
            var header = document.getElementById('header');
            header.innerHTML = "Ask a question";
            var button = document.getElementById('send');
            button.innerHTML = "Send";
            button.disabled = false;
            var p = messages.lastChild.lastChild;
            p.innerHTML += data.message;
        }
    } else {
        var div = document.createElement('div');
        div.className = 'client-message';
        var p = document.createElement('p');
        p.innerHTML = "<strong>" + "You: " + "</strong>";
        p.innerHTML += data.message;
        div.appendChild(p);
        messages.appendChild(div);
    }
    // Scroll to the bottom of the chat
    messages.scrollTop = messages.scrollHeight;
};
// Send message to server
function sendMessage(event) {
    event.preventDefault();
    var message = document.getElementById('messageText').value;
    if (message === "") {
        return;
    }
    ws.send(message);
    document.getElementById('messageText').value = "";

    // Turn the button into a loading button
    var button = document.getElementById('send');
    button.innerHTML = "Loading...";
    button.disabled = true;
}

