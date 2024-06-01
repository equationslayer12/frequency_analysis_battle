import Protocol from "@/webclient/Protocol";
import SessionHandle from "@/webclient/Sessions/SessionHandle";
import User from "./User";
import { defaultUsername } from "@/Constants";

export class ClientUser extends User {
    constructor(username: string) {
        super(username);
    }

    /**
     * Updates username from the username cookie. it is changeable by the user,
     * but it should'nt be a big deal. unless?
     */
    updateFromSession() {
        let username = SessionHandle.getCookie("username");
        if (!username)
            return;
        this.username.value = Protocol.Sessions.decryptUsername(username);
    }

    logIn() {
        this.updateFromSession();
        this.isGuest.value = false;
    }

    logOut() {
        this.username.value = defaultUsername;
        this.isGuest.value = true;
    }
}

export default new ClientUser(defaultUsername);
