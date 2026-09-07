export class Body {
    constructor(root) {
        const messages = root.querySelector('[data-messages]');
        if (!messages) {
            throw new Error('Body requires an element with data-messages.');
        }
        this.messages = messages;
    }
    addSentMessage(text, time = 'baru saja') {
        this.addMessage({
            name: 'Kamu',
            initials: 'YO',
            text,
            time,
        }, true);
    }
    addReceivedMessage(message) {
        this.addMessage(message, false);
    }
    addSystemMessage(text) {
        const message = document.createElement('div');
        message.className = 'system-message';
        message.textContent = text;
        this.messages.appendChild(message);
        this.scrollToLatest();
    }
    scrollToLatest() {
        this.messages.scrollTop = this.messages.scrollHeight;
    }
    addMessage(message, isMine) {
        const article = document.createElement('article');
        article.className = isMine ? 'message mine' : 'message';
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.setAttribute('aria-hidden', 'true');
        avatar.textContent = message.initials;
        const content = document.createElement('div');
        content.className = 'message-content';
        const meta = document.createElement('div');
        meta.className = 'message-meta';
        const name = document.createElement('span');
        name.className = 'message-name';
        name.textContent = message.name;
        const time = document.createElement('span');
        time.className = 'message-time';
        time.textContent = message.time ?? 'baru saja';
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = message.text;
        meta.append(name, time);
        content.append(meta, bubble);
        article.append(avatar, content);
        this.messages.appendChild(article);
        this.scrollToLatest();
    }
}
