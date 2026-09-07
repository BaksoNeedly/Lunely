export type SendMessageHandler = (message: string) => void;

export class Footer {
    private readonly form: HTMLFormElement;
    private readonly input: HTMLInputElement;
    private sendMessageHandler: SendMessageHandler | null = null;

    public constructor(root: HTMLElement) {
        const form = root.querySelector<HTMLFormElement>('[data-composer]');
        const input = root.querySelector<HTMLInputElement>('[data-message-input]');
        if (!form || !input) {
            throw new Error('Footer requires a composer form and message input.');
        }

        this.form = form;
        this.input = input;
        this.form.addEventListener('submit', (event) => this.handleSubmit(event));
    }

    public onSendMessage(handler: SendMessageHandler): void {
        this.sendMessageHandler = handler;
    }

    private handleSubmit(event: SubmitEvent): void {
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
