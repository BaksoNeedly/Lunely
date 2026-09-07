export interface ChatMessage {
    name: string;
    initials: string;
    text: string;
    time?: string;
}

export class Body {
    private readonly messages: HTMLElement;

    public constructor(root: HTMLElement) {
        const messages = root.querySelector<HTMLElement>('[data-messages]');
        if (!messages) {
            throw new Error('Body requires an element with data-messages.');
        }

        this.messages = messages;
    }

    public addSentMessage(text: string, time = 'baru saja'): void {
        this.addMessage({
            name: 'Kamu',
            initials: 'YO',
            text,
            time,
        }, true);
    }

    public addReceivedMessage(message: ChatMessage): void {
        this.addMessage(message, false);
    }

    public addSystemMessage(text: string): void {
        const message = document.createElement('div');
        message.className = 'system-message';
        message.textContent = text;
        this.messages.appendChild(message);
        this.scrollToLatest();
    }

    public scrollToLatest(): void {
        this.messages.scrollTop = this.messages.scrollHeight;
    }

    private addMessage(message: ChatMessage, isMine: boolean): void {
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
