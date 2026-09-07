export class Footer {
    constructor(root) {
        this.sendMessageHandler = null;
        const form = root.querySelector('[data-composer]');
        const input = root.querySelector('[data-message-input]');
        if (!form || !input) {
            throw new Error('Footer requires a composer form and message input.');
        }
        this.form = form;
        this.input = input;
        this.form.addEventListener('submit', (event) => this.handleSubmit(event));
    }
    onSendMessage(handler) {
        this.sendMessageHandler = handler;
    }
    handleSubmit(event) {
        event.preventDefault();
        const message = this.input.value.trim();
        if (!message || !this.sendMessageHandler) {
            return;
        }
        this.sendMessageHandler(message);
        this.input.value = '';
        this.input.focus();
    }
}
