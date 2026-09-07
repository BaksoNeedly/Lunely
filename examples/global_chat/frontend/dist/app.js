import { Body } from './body.js';
import { Footer } from './footer.js';
import { Header } from './header.js';
const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${location.host}/`);
socket.onopen = () => {
    console.log('WebSocket connected');
    socket.send(JSON.stringify({
        "type": "user_join",
        "data": {}
    }));
};
socket.onmessage = (event) => {
    const packet = JSON.parse(event.data);
    const type = packet["type"];
    const data = packet["data"];
    switch (type) {
        case "user_join_message":
            body.addSystemMessage(data["username"] + " Joined");
            break;
        case "message":
            body.addReceivedMessage({
                name: 'Anonymous',
                initials: 'EY',
                text: data["content"],
                time: "baru tadi"
            });
            break;
    }
};
socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};
socket.onclose = (event) => {
    console.log('WebSocket closed:', event.code, event.reason);
};
const headerElement = document.querySelector('[data-header]');
const bodyElement = document.querySelector('[data-body]');
const footerElement = document.querySelector('[data-footer]');
if (!headerElement || !bodyElement || !footerElement) {
    throw new Error('Chat app requires header, body, and footer elements.');
}
const header = new Header(headerElement);
const body = new Body(bodyElement);
const footer = new Footer(footerElement);
footer.onSendMessage((message) => {
    body.addSentMessage(message);
    socket.send(JSON.stringify({
        "type": "message",
        "content": message
    }));
});
header.setOnline(128);
window.chatApp = { header, body, footer };
