export class Header {
    private readonly onlineCount: HTMLElement;

    public constructor(root: HTMLElement) {
        const onlineCount = root.querySelector<HTMLElement>('[data-online-count]');
        if (!onlineCount) {
            throw new Error('Header requires an element with data-online-count.');
        }

        this.onlineCount = onlineCount;
    }

    public setOnline(count: number): void {
        if (!Number.isFinite(count) || count < 0) {
            throw new Error('Online count must be a non-negative number.');
        }

        this.onlineCount.textContent = `${Math.floor(count)} orang online`;
    }
}
