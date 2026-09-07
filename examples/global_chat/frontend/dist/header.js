export class Header {
    constructor(root) {
        const onlineCount = root.querySelector('[data-online-count]');
        if (!onlineCount) {
            throw new Error('Header requires an element with data-online-count.');
        }
        this.onlineCount = onlineCount;
    }
    setOnline(count) {
        if (!Number.isFinite(count) || count < 0) {
            throw new Error('Online count must be a non-negative number.');
        }
        this.onlineCount.textContent = `${Math.floor(count)} orang online`;
    }
}
