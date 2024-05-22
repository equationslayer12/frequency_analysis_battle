/**
 * A class that provides an asynchronous lock mechanism. This can be used to ensure
 * that a particular piece of code is only executed by one async operation at a time,
 * preventing race conditions and ensuring sequential execution of critical sections.
 */
class AsyncLock {
    private queue: (() => void)[] = [];
    private isLocked: boolean = false;

    /**
     * Acquires the lock. If the lock is already held, the promise will be queued
     * and resolved when the lock is released.
     * 
     * @returns {Promise<void>} A promise that resolves when the lock is acquired.
     */
    async acquire(): Promise<void> {
        if (!this.isLocked) {
            this.isLocked = true;
            return;
        }

        return new Promise<void>((resolve) => {
            this.queue.push(resolve);
        });
    }

    /**
     * Releases the lock. If there are any queued promises, the next one in the queue
     * will be resolved, transferring the lock to it. If the queue is empty, the lock
     * will be released.
     */
    release(): void {
        if (this.queue.length > 0) {
            const nextResolve = this.queue.shift();
            if (nextResolve) {
                nextResolve();
            }
        } else {
            this.isLocked = false;
        }
    }
}
