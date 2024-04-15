export default class SessionUtils {
    static getCookie(cookieName: string) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${cookieName}=`);
        if (parts.length === 2)
            return parts.pop()?.split(';').shift();
    }

    static encryptUsername(username: string) {
        return username;
    }

    static decryptUsername(username: string) {
        return username;
    }
}
