export default class SessionHandle {
    static getCookie(cookieName: string) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${cookieName}=`);
        if (parts.length === 2)
            return parts.pop()?.split(';').shift();
    }
}
